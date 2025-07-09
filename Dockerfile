# Dockerfile
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/
COPY docs/ ./docs/
COPY .env .env

# Crear directorio para ChromaDB
RUN mkdir -p chroma_db

# Exponer puerto
EXPOSE 8000

# Variables de entorno
ENV PYTHONPATH=/app
ENV HOST=0.0.0.0
ENV PORT=8000

# Comando para ejecutar la aplicación
CMD ["python", "-m", "src.api.main"]
