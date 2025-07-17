# Dockerfile para contenerizar la aplicación Flask de Pokédex
# Usa Python 3.10 slim como base
FROM python:3.10-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea el directorio de la app
WORKDIR /app

# Copia los archivos de la aplicación
COPY . /app

# Instala las dependencias de Python
RUN pip install --upgrade pip && pip install -r Poke/poke/app/requirements.txt

# Expone el puerto de Flask
EXPOSE 5000

# Comando para iniciar la app
CMD ["python", "Poke/poke/app/poke.py"]
