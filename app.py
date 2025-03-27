# Import potřebných knihoven
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any
import numpy as np

# Nastavení konfigurace stránky Streamlit
st.set_page_config(
    page_title="Czech Republic Crime Statistics",
    page_icon="🇨🇿",
    layout="wide"    #Široké rozvržení pro lepší zobrazení grafů
)

# URL adresa API, odkud načítáme data
API_URL = "http://fastapi:8000"

# === Funkce pro načtení dat z API s kešováním výsledků ===
@st.cache_data(ttl=3600)
def load_crime_types():
    response = requests.get(f"{API_URL}/crime-types")
    return response.json()

@st.cache_data(ttl=3600)
def load_areas():
    response = requests.get(f"{API_URL}/areas")
    return response.json()

@st.cache_data(ttl=3600)
def load_years():
    response = requests.get(f"{API_URL}/years")
    return response.json()

@st.cache_data(ttl=300)
def load_crime_data(year=None, crime_type_id=None):
    params = {}
    if year:
        params["year"] = year
    if crime_type_id:
        params["crime_type_id"] = crime_type_id
    
    response = requests.get(f"{API_URL}/crime-data", params=params)
    return response.json()

# === Funkce pro vizualizaci dat ===
def create_crime_bar_chart(crime_data, selected_year, selected_crime_type):
    """Create a bar chart of crime by region"""
    filtered_data = [
        item for item in crime_data 
        if item["year"] == selected_year and item["crime_type_id"] == selected_crime_type
    ]
    
    df = pd.DataFrame(filtered_data)    # Převod na DataFrame
    
    if df.empty:
        return None         # Pokud nejsou žádná data, vrátíme None
    
    df = df[df["area_id"] > 1]        # Vynechání celkových dat za ČR
    
     # Seřazení podle počtu trestných činů (od nejvyššího po nejnižší)
    df_sorted = df.sort_values("count", ascending=False)
    
     # Vytvoření sloupcového grafu
    fig = px.bar(
        df_sorted,
        x="area_name",
        y="count",
        title=f"Crime Counts by Region ({selected_year})",
        color="count",
        color_continuous_scale="RdYlGn_r",   # Červená = vysoká kriminalita, zelená = nízká
        labels={"area_name": "Region", "count": "Crime Count"}
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        xaxis_title="Region",
        yaxis_title="Crime Count",
        coloraxis_showscale=False,
        height=500,
    )
    
    return fig        # Vrácení grafu

def create_crime_trend_chart(crime_data, selected_crime_type):
    """Create a line chart showing crime trends over years"""
    # Filter for the selected crime type
    filtered_data = [
        item for item in crime_data 
        if item["crime_type_id"] == selected_crime_type
    ]
    
    df = pd.DataFrame(filtered_data)
    
    if df.empty:
        return None
    
    # Get data for all regions except the whole country
    df = df[df["area_id"] > 1]
    
    # Group by year and region
    df_grouped = df.groupby(["year", "area_name"])["count"].sum().reset_index()
    
    # Create line chart
    fig = px.line(
        df_grouped, 
        x="year", 
        y="count", 
        color="area_name",
        title=f"Crime Trends by Region",
        labels={"count": "Crime Count", "year": "Year", "area_name": "Region"}
    )
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Crime Count",
        legend_title="Region",
        height=500,
    )
    
    return fig
def create_crime_comparison_chart(crime_data, selected_year):
    """Create a grouped bar chart comparing crime types"""
    # Filter for the selected year
    filtered_data = [
        item for item in crime_data 
        if item["year"] == selected_year
    ]
    
    df = pd.DataFrame(filtered_data)
    
    if df.empty:
        return None
    
    # Get data for all regions except the whole country
    df = df[df["area_id"] > 1]
    
    # Create grouped bar chart
    fig = px.bar(
        df,
        x="area_name",
        y="count",
        color="crime_type",
        title=f"Crime Types by Region ({selected_year})",
        barmode="group",
        labels={"area_name": "Region", "count": "Crime Count", "crime_type": "Crime Type"}
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        xaxis_title="Region",
        yaxis_title="Crime Count",
        legend_title="Crime Type",
        height=500,
    )
    
    return fig

def create_total_crime_by_type(crime_data, selected_year):
    """Create a pie chart showing total crime by type"""
    # Filter for the selected year and whole country (area_id = 1)
    filtered_data = [
        item for item in crime_data 
        if item["year"] == selected_year and item["area_id"] == 1
    ]
    
    df = pd.DataFrame(filtered_data)
    
    if df.empty:
        return None
    
    # Create pie chart
    fig = px.pie(
        df,
        values="count",
        names="crime_type",
        title=f"Distribution of Crime Types in Czech Republic ({selected_year})",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    
    return fig

def create_combined_sunburst_treemap(crime_data, hierarchy):
    """Create a combined sunburst and treemap visualization with a user-defined hierarchy."""
    df = pd.DataFrame(crime_data)
    
    if df.empty:
        return None, None
    
    # Filter out "kriminalita celkem" (assuming its identifier or description is "kriminalita celkem")
    df = df[~df["crime_type"].str.contains("kriminalita celkem", case=False, na=False)]
    
    # Create sunburst chart
    sunburst_fig = px.sunburst(
        df,
        path=hierarchy,
        values="count",
        title="Crime Distribution (Sunburst)",
        color="count",
        color_continuous_scale="RdYlGn_r",
        labels={"year": "Year", "crime_type": "Crime Type", "area_name": "Region", "count": "Crime Count"}
    )
    sunburst_fig.update_layout(height=500)
    
    # Create treemap
    treemap_fig = px.treemap(
        df,
        path=hierarchy,
        values="count",
        title="Crime Distribution (Treemap)",
        color="count",
        color_continuous_scale="RdYlGn_r",
        labels={"year": "Year", "crime_type": "Crime Type", "area_name": "Region", "count": "Crime Count"}
    )
    treemap_fig.update_layout(height=500)
    
    return sunburst_fig, treemap_fig

def create_user_bar_chart(user_data, x_column, y_column):
    """Create a bar chart from the user's uploaded data."""
    if x_column not in user_data.columns or y_column not in user_data.columns:
        return None
    
    fig = px.bar(
        user_data,
        x=x_column,
        y=y_column,
        title="User Uploaded Data - Bar Chart",
        labels={x_column: "X-Axis", y_column: "Y-Axis"},
        color=y_column,
        color_continuous_scale="RdYlGn_r"
    )
    
    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column,
        height=500,
    )
    
    return fig

def calculate_total_crime(crime_data):
    """Calculate total crime ('kriminalita celkem') for each year."""
    df = pd.DataFrame(crime_data)
    
    if df.empty:
        return None
    
    # Filter for "kriminalita celkem" (assuming its identifier or description is "kriminalita celkem")
    total_crime_df = df[df["crime_type"].str.contains("kriminalita celkem", case=False, na=False)]
    
    # Group by year and sum the counts
    total_crime_by_year = total_crime_df.groupby("year")["count"].sum().reset_index()
    total_crime_by_year.rename(columns={"count": "total_crime"}, inplace=True)
    
    return total_crime_by_year

def create_total_crime_bar_chart(total_crime_data):
    """Create a bar chart for total crime by year."""
    if total_crime_data is None or total_crime_data.empty:
        return None
    
    fig = px.bar(
        total_crime_data,
        x="year",
        y="total_crime",
        title="Total Crime by Year",
        labels={"year": "Year", "total_crime": "Total Crime"},
        color="total_crime",
        color_continuous_scale="RdYlGn_r"
    )
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Crime",
        height=400,
    )
    
    return fig

# === Hlavní aplikace ===
def main():
        # Titulek aplikace
    st.title("🇨🇿 Czech Republic Crime Statistics")
    st.write("Explore crime statistics across different regions of the Czech Republic")
    
    # Load the necessary data
    try:
         # Načtení dat z API
        crime_types = load_crime_types()    # Načtení typů kriminality
        #areas = load_areas()
        years = load_years()                # Načtení dostupných let
        print(years)
        # Create sidebar for filters
        st.sidebar.header("Filters")         # Nadpis bočního panelu
        
         # Převod typů kriminality na slovník pro snadný výběr
        crime_type_dict = {ct["id"]: ct["description"] for ct in crime_types}
        
        # Výchozí hodnoty filtrů
        default_crime_type = 1
        
        # Výběr typu kriminality
        selected_crime_type = st.sidebar.selectbox(
            "Select Crime Type:",
            options=list(crime_type_dict.keys()),
            format_func=lambda x: crime_type_dict[x],
            index=list(crime_type_dict.keys()).index(default_crime_type) if default_crime_type in crime_type_dict else 0
        )
        
        # Získání nejnovějšího roku jako výchozí hodnota
        default_year = max(years) if years else None

        # Výběr roku pomocí bočního panelu
        selected_year = st.sidebar.selectbox(
            "Select Year:",
            options=years,
            index=years.index(default_year) if default_year in years else 0
        )
        
       # Načtení všech dat o kriminalitě najednou
        all_crime_data = load_crime_data()
        
         # Výpočet celkového počtu trestných činů pro každý rok
        total_crime_data = calculate_total_crime(all_crime_data)
        
        # Zobrazení celkových statistik kriminality v bočním panelu
        st.sidebar.header("Total Crime Statistics")
        if total_crime_data is not None and not total_crime_data.empty:
            st.sidebar.subheader("Total Crime by Year")
            st.sidebar.dataframe(total_crime_data)    # Zobrazení datového rámce s celkovými počty
            
              # Přidání sloupcového grafu s celkovým počtem trestných činů podle roku
            total_crime_chart = create_total_crime_bar_chart(total_crime_data)
            if total_crime_chart:
                st.sidebar.plotly_chart(total_crime_chart, use_container_width=True)
        else:
            st.sidebar.info("No total crime data available.")
        
        # Vytvoření záložek pro různé vizualizace
        tab1, tab2, tab3, tab4 = st.tabs([
            "Crime by Region", 
            "Crime Trends", 
            "Crime Types Comparison", 
            "Crime Distribution"
        ])

        # === Záložka: Kriminalita podle regionu ===
        with tab1:
            st.subheader("Crime Counts by Region")
            
            if all_crime_data:
                bar_chart = create_crime_bar_chart(all_crime_data, selected_year, selected_crime_type)
                if bar_chart:
                    st.plotly_chart(bar_chart, use_container_width=True)
                else:
                    st.info("No data available for the selected filters.")
                
                 # Zobrazení názvu vybraného typu kriminality
                crime_type_name = crime_type_dict.get(selected_crime_type, "Unknown")
                st.write(f"Selected Crime Type: {crime_type_name}")
            else:
                st.info("No crime data available.")

        # === Záložka: Trendy kriminality ===
        with tab2:
            st.subheader("Crime Trends Over Time")
            
            if all_crime_data:
                trend_chart = create_crime_trend_chart(all_crime_data, selected_crime_type)
                if trend_chart:
                    st.plotly_chart(trend_chart, use_container_width=True)
                else:
                    st.info("No trend data available for the selected crime type.")
            else:
                st.info("No crime data available.")

        # === Záložka: Porovnání typů kriminality ===
        with tab3:
            st.subheader("Comparison of Crime Types by Region")
            
            if all_crime_data:
                comparison_chart = create_crime_comparison_chart(all_crime_data, selected_year)
                if comparison_chart:
                    st.plotly_chart(comparison_chart, use_container_width=True)
                else:
                    st.info("No comparison data available for the selected year.")
            else:
                st.info("No crime data available.")

        # === Záložka: Distribuce kriminality (Sunburst a Treemap) ===
        with tab4:
            st.subheader("Crime Distribution - Sunburst and Treemap")

            # Výběr hierarchie pro vizualizaci Sunburst a Treemap
            if all_crime_data:
                # Allow user to select hierarchy for Sunburst and Treemap
                st.sidebar.header("Hierarchy Options")
                st.sidebar.info("Note: This option affects only the 'Crime Distribution' section.")  # Added user note
                hierarchy_options = [
                    ["year", "crime_type", "area_name"],    # Hierarchie: Rok > Typ kriminality > Region
                    ["area_name", "crime_type", "year"],     # Hierarchie: Region > Typ kriminality > Rok
                    ["crime_type", "year", "area_name"]    # Hierarchie: Typ kriminality > Rok > Region
                ]
                selected_hierarchy = st.sidebar.selectbox(
                    "Select Hierarchy:",
                    options=hierarchy_options,
                    format_func=lambda x: " > ".join(x)    # Zobrazení hierarchie jako text
                )

                 # Vytvoření vizualizací Sunburst a Treemap
                sunburst_chart, treemap_chart = create_combined_sunburst_treemap(all_crime_data, selected_hierarchy)
                if sunburst_chart and treemap_chart:
                    st.plotly_chart(sunburst_chart, use_container_width=True)
                    st.plotly_chart(treemap_chart, use_container_width=True)
                else:
                    st.info("No distribution data available.")
            else:
                st.info("No crime data available.")

    # Ošetření chyb
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Check if the backend API is running correctly.")

# Spuštění aplikace
if __name__ == "__main__":
    main()
