# 1. Usar una imagen oficial y liviana de Python
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar los archivos necesarios al contenedor
COPY cargar_en_postgres.py .
COPY ml-artifacts/ ./ml-artifacts/

# 4. Instalar las librerías directamente dentro de Docker (sin entornos virtuales locales)
RUN pip install --no-cache-dir pandas psycopg2-binary

# 5. Comando que se ejecutará al arrancar el contenedor
CMD ["python", "cargar_en_postgres.py"]