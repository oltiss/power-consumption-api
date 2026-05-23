FROM python:3.12-slim

# Instalacja podstawowych narzędzi sieciowych dla tinytuya
RUN apt-get update && apt-get install -y \
    iputils-ping \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Kopiujemy listę bibliotek i instalujemy je
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy cały nasz kod (oraz pliki json, jeśli już istnieją)
COPY . .

# Domyślnie Docker uruchomi naszą aplikację FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
