# Používáme oficiální obraz Pythonu verze 3.10
FROM python:3.10

# Nastavíme pracovní adresář uvnitř kontejneru
WORKDIR /app

# Zkopírujeme soubor s požadavky (závislostmi) do kontejneru
COPY requirements.txt requirements.txt

# Nainstalujeme závislosti ze souboru requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Zkopírujeme celý kód aplikace do kontejneru
COPY . .

# Spustíme aplikaci pomocí Uvicorn (server pro FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
