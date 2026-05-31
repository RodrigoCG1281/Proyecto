#!/usr/bin/env python3
"""
Carga masiva del entregable CSV a PostgreSQL usando psycopg2.
"""

import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Parámetros de conexión que coinciden con nuestro docker-compose
DB_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "database": "ecommerce_vectorial",
    "user": "postgres",
    "password": "password"
}

CSV_EMBEDDINGS_PATH = "ml-artifacts/embeddings/item_embeddings.csv"

def ejecutar_carga_masiva():
    # 1. Verificar si el archivo con embeddings existe
    if not os.path.exists(CSV_EMBEDDINGS_PATH):
        print(f"Error: No se encuentra el archivo consolidado en {CSV_EMBEDDINGS_PATH}")
        print("Por favor, ejecuta primero 'generar_embeddings.py'.")
        return

    print(f"Cargando datos desde el entregable intermedio: {CSV_EMBEDDINGS_PATH}...")
    df = pd.read_csv(CSV_EMBEDDINGS_PATH)

    # 2. Preparar las tuplas con el orden exacto de las columnas de la BD
    # product_id, name, description, embedding
    registros = []
    for row in df.itertuples(index=False):
        # row[0]=product_id, row[1]=name, row[2]=description, row[3]=embedding
        nombre_truncado = str(row.name)[:255] 
        registros.append((row.product_id, nombre_truncado, row.description, row.embedding))

    conn = None
    try:
        print("Conectando al servidor PostgreSQL en Docker...")
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Usamos execute_values junto con ON CONFLICT por idempotencia
        insert_query = """
            INSERT INTO products (product_id, name, description, embedding)
            VALUES %s
            ON CONFLICT (product_id) 
            DO UPDATE SET 
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                embedding = EXCLUDED.embedding;
        """

        print(f"Iniciando inserción masiva de {len(registros)} productos con vectores...")
        execute_values(cur, insert_query, registros)
        
        # Confirmar la transacción
        conn.commit()
        print("¡Carga masiva completada con éxito en la base de datos vectorial!")

    except Exception as e:
        print(f"Error crítico durante la carga en Postgres: {e}")
        if conn:
            conn.rollback()
            print("Se aplicó un rollback para mantener la consistencia de los datos.")
            
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Conexión cerrada de forma segura.")

if __name__ == "__main__":
    ejecutar_carga_masiva()