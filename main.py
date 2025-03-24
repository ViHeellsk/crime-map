from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os

app = FastAPI(title="Crime Map API")

# Povolení CORS, aby API mohlo přijímat požadavky z jakéhokoli zdroje
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Povolení požadavků ze všech domén
    allow_credentials=True,
    allow_methods=["*"],  # Povolení všech metod (GET, POST atd.)
    allow_headers=["*"],
)

# Funkce pro připojení k databázi
def get_db():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="mariadb",  # Hostitel databáze
            database="crime_map",  # Název databáze
            user="root",  # Uživatelské jméno
            password="1234"  # Heslo
        )
        return connection
    except Error as e:
        print(f"Chyba při připojení k MariaDB: {e}")
        raise HTTPException(status_code=500, detail="Chyba připojení k databázi")

  # Modely dat
class CrimeType(BaseModel):
    id: int
    description: str  # Název typu trestného činu

class Area(BaseModel):
    id: int
    name: str
    geojson_data: Optional[dict] = None  # Geografická data ve formátu GeoJSON

class CrimeData(BaseModel):
    area_id: int
    crime_type_id: int
    year: int
    count: int  # Počet trestných činů

# Hlavní cesta API
@app.get("/")
def read_root():
    return {"message": "Vítejte v Czech Crime Map API"}

# Získání seznamu typů trestných činů
@app.get("/crime-types", response_model=List[CrimeType])
def get_crime_types(connection=Depends(get_db)):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id_crime_type as id, description FROM id_catalog")
        crime_types = cursor.fetchall()
        cursor.close()
        connection.close()
        return crime_types
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Získání seznamu oblastí a jejich hranic ve formátu GeoJSON
@app.get("/areas", response_model=List[Area])
def get_areas(connection=Depends(get_db)):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id_area as id, name, geojson_data FROM id_area")
        areas = cursor.fetchall()
        cursor.close()
        connection.close()

    # Převod geojson_data z řetězce na JSON
        for area in areas:
            if area["geojson_data"] and area["geojson_data"] != "[NULL]":
                try:
                    area["geojson_data"] = json.loads(area["geojson_data"])
                except:
                    area["geojson_data"] = None
        
        return areas
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

  # Získání dat o trestných činech (filtrováno podle roku a typu trestného činu)
@app.get("/crime-data")
def get_crime_data(year: Optional[int] = None, crime_type_id: Optional[int] = None, connection=Depends(get_db)):
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT a.id_area as area_id, a.name as area_name, c.id_crime_type as crime_type_id, 
               ct.description as crime_type, c.year, c.count
        FROM crimes c
        JOIN id_area a ON c.id_area = a.id_area
        JOIN id_catalog ct ON c.id_crime_type = ct.id_crime_type
        WHERE 1=1
        """
        params = []
        
        if year:
            query += " AND c.year = %s"
            params.append(year)
        
        if crime_type_id:
            query += " AND c.id_crime_type = %s"
            params.append(crime_type_id)
        
        cursor.execute(query, params)
        crime_data = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return crime_data
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

  # Získání dostupných let
@app.get("/years")
def get_available_years(connection=Depends(get_db)):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT year FROM crimes ORDER BY year")
        years = [item["year"] for item in cursor.fetchall()]
        cursor.close()
        connection.close()
        return years
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

  # Získání GeoJSON souboru s hranicemi České republiky
@app.get("/geojson")
def get_geojson():
    try:
        # Cesta k souboru GeoJSON
        file_path = os.path.join(os.path.dirname(__file__), "mariadb_data", "czech_republic.geojson")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                geojson_data = json.load(f)
            return geojson_data
        else:
            raise HTTPException(status_code=404, detail="GeoJSON soubor nebyl nalezen")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

  # Spuštění API pomocí Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
