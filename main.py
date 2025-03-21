# Importujeme potřebné knihovny
from fastapi import FastAPI, File, UploadFile, HTTPException  # FastAPI pro API
import pandas as pd  # Knihovna pro práci s daty (CSV, Excel)
import mysql.connector  # Konektor pro připojení k MySQL/MariaDB
import io  # Pomáhá zpracovat soubory v paměti

# Inicializace FastAPI aplikace
app = FastAPI()

# Konfigurace databáze
db_config = {
    "host": "mariadb",  # Název databázového serveru
    "user": "root",  # Uživatelské jméno
    "password": "1236",  # Heslo
    "database": "crime_map"  # Název databáze
}

def insert_crime_data(df):
    conn = mysql.connector.connect(**db_config)  # Připojení k databázi
    cursor = conn.cursor()

# SQL dotaz pro vložení dat do tabulky crime_data
    query = """
    INSERT INTO crime_data (area_id, year, crime_type_id, count)
    VALUES (%s, %s, %s, %s)
    """

# Projdeme řádky DataFrame a vložíme je do databáze
    for _, row in df.iterrows():
        cursor.execute(query, (row["area_id"], row["year"], row["crime_type_id"], row["count"]))

    conn.commit()  # Uložíme změny
    cursor.close()
    conn.close()  # Uzavřeme připojení

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()  # Načteme obsah souboru
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))  # Převedeme na DataFrame
        
        # Ověříme, zda soubor obsahuje požadované sloupce
        if not {"area_id", "year", "crime_type_id", "count"}.issubset(df.columns):
            raise HTTPException(status_code=400, detail="Chybí požadované sloupce!")

        insert_crime_data(df)  # Vložíme data do databáze
        return {"message": "Data byla úspěšně nahrána!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Vrátíme chybu v případě problémů

@app.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...)):
    """Endpoint pro nahrání Excel souboru s daty kriminality."""
    try:
        contents = await file.read()  # Načteme obsah souboru
        df = pd.read_excel(io.BytesIO(contents))  # Převedeme na DataFrame

        # Ověříme, zda soubor obsahuje požadované sloupce
        if not {"area_id", "year", "crime_type_id", "count"}.issubset(df.columns):
            raise HTTPException(status_code=400, detail="Chybí požadované sloupce!")

        insert_crime_data(df)  # Vložíme data do databáze
        return {"message": "Data byla úspěšně nahrána!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Vrátíme chybu v případě problémů
