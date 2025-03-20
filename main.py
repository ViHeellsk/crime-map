# Importujeme potřebné knihovny
from fastapi import FastAPI, File, UploadFile, HTTPException  # FastAPI pro API
import pandas as pd  # Knihovna pro práci s daty (CSV, Excel)
import mysql.connector  # Konektor pro připojení k MySQL/MariaDB
import io  # Pomáhá zpracovat soubory v paměti

# Inicializace FastAPI aplikace
app = FastAPI()

# Konfigurace databáze (změňte podle svého nastavení)
db_config = {
    "host": "mariadb",  # Název databázového serveru
    "user": "root",  # Uživatelské jméno
    "password": "1236",  # Heslo
    "database": "crime_map"  # Název databáze
}

def insert_crime_data(df):
    conn = mysql.connector.connect(**db_config)  # Připojení k databázi
    cursor = conn.cursor()
