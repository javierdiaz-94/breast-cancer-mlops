# Imagen base oficial de Python
FROM python:3.9-slim

# Metadatos
LABEL maintainer="MLOps Team"
LABEL description="Breast Cancer Prediction API"
LABEL version="1.0.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000 \
    DEBUG=False

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema si son necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY models/ ./models/
COPY api/ ./api/

# Crear usuario no privilegiado para ejecutar la aplicación
RUN useradd -m -u 1000 apiuser && \
    chown -R apiuser:apiuser /app

# Cambiar a usuario no privilegiado
USER apiuser

# Exponer puerto
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/')" || exit 1

# Comando para ejecutar la aplicación
CMD ["python", "api/app.py"]