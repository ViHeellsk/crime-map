from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List
import pandas as pd 


# Připojení k databázi MySQL
#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://pepa:semtex123.@mariadb/interesting_places_db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:example@mariadb/Interesting_Places"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definice modelu pro dotazy na místa
class Place(BaseModel):
    place_name: str
    latitude: float
    longitude: float
    description: str
    language: str

# Inicializace FastAPI
app = FastAPI()

# Endpoint pro získání všech míst
@app.get("/places/", response_model=List[Place])
def read_places(skip: int = 0, limit: int = 100):
    '''
    Popis funkcionality places
    vstup:
    skip - kolik zaznamu mam na pocatku vynechat
    limit - kolik zaznamu chci ziskat
    vystup:
    zaznamy o zajimavych mistech
    '''
    db = SessionLocal()
    query = text("SELECT place_name, latitude, longitude, description, language FROM Interesting_Places LIMIT :limit OFFSET :skip")
    result = db.execute(query, {"limit": limit, "skip": skip}).fetchall()
    return result


@app.get("/data/", response_model=List[Place])
def read_places(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    query = text("SELECT place_name, latitude, longitude, description, language FROM Interesting_Places LIMIT :limit OFFSET :skip")
    result = db.execute(query, {"limit": limit, "skip": skip}).fetchall()
    return result


# Spuštění FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

