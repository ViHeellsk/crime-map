--Vytvořme databázi, pokud ještě neexistuje
CREATE DATABASE IF NOT EXISTS crime_map; 
USE crime_map;

-- Tabulka pro ukládání druhů kriminality
CREATE TABLE IF NOT EXISTS crime_catalog ( 
    id INT AUTO_INCREMENT PRIMARY KEY, --ID typu zločinu 
    crime_type VARCHAR(50),             -- nazev druhu zločinu
    description TEXT                    -- Popis zločinu
);

-- Tabulka pro ukládání informací o městech (oblastech)
CREATE TABLE IF NOT EXISTS crime_areas (
    id INT AUTO_INCREMENT PRIMARY KEY,    -- Unikátní ID města
    name VARCHAR(100),                    -- Název města (např. "Praha", "Brno")
    geojson_data JSON                    -- Geografická data (používají se pro zobrazení na mapě)
);

-- Tabulka pro ukládání statistik kriminality
CREATE TABLE IF NOT EXISTS crime_data (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- Unikátní ID záznamu
    area_id INT,                              -- ID města (odkaz na crime_areas)  
    year INT,                                -- Rok, za který jsou data shromážděna
    crime_type_id INT,                        -- ID typu trestného činu (odkaz na crime_catalog)
    count INT,                                -- Počet trestných činů
     -- Vazba na tabulku měst (crime_areas)
    FOREIGN KEY (area_id) REFERENCES crime_areas(id),
    -- Vazba na tabulku typů trestných činů (crime_catalog)
    FOREIGN KEY (crime_type_id) REFERENCES crime_catalog(id)
);
