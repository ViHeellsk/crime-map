CREATE DATABASE IF NOT EXISTS crime_map;
USE crime_map;

CREATE TABLE IF NOT EXISTS crime_catalog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crime_type VARCHAR(50),
    description TEXT
);

CREATE TABLE IF NOT EXISTS crime_areas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    geojson_data JSON
);

CREATE TABLE IF NOT EXISTS crime_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    area_id INT,
    year INT,
    crime_type_id INT,
    count INT,
    FOREIGN KEY (area_id) REFERENCES crime_areas(id),
    FOREIGN KEY (crime_type_id) REFERENCES crime_catalog(id)
);
