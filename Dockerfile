# Použijeme oficiální obraz Pythonu jako základ
FROM python:3.9

# Vytvoříme a nastavíme pracovní adresář ve stroji
WORKDIR /app

# Nakopírujeme soubory s kódem aplikace do pracovního adresáře ve stroji
COPY . /app

# Nainstalujeme závislosti pomocí pip (Předpokládejme, že máme requirements.txt se závislostmi)
RUN pip install --no-cache-dir -r requirements.txt

# Exponujeme port 8000, který používá FastAPI
EXPOSE 8000

# Spustíme FastAPI aplikaci pomocí uvicorn serveru
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

