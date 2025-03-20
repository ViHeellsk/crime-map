# Importujeme potřebné knihovny
from fastapi import FastAPI, File, UploadFile, HTTPException  # FastAPI pro API
import pandas as pd  # Knihovna pro práci s daty (CSV, Excel)
import mysql.connector  # Konektor pro připojení k MySQL/MariaDB
import io  # Pomáhá zpracovat soubory v paměti

# Inicializace FastAPI aplikace
app = FastAPI()
