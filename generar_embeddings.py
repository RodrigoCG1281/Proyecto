#!/usr/bin/env python3
"""
Dataset: https://www.kaggle.com/code/mehakiftikhar/amazon-sales-dataset-eda/input
Fase 1: Extracción del dataset de Amazon y Generación de Embeddings locales - Rodrigo
"""

import os
import pandas as pd
from sentence_transformers import SentenceTransformer

# Configuración de rutas
INPUT_CSV = "amazon.csv"  # El archivo descargado de Kaggle
OUTPUT_DIR = "ml-artifacts/embeddings"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "item_embeddings.csv")


def pipeline_generacion_embeddings():
    # 1. Validar que el archivo de origen exista
    if not os.path.exists(INPUT_CSV):
        print(
            f"Error: No se encuentra el archivo '{INPUT_CSV}' en la raíz."
        )
        print("Por favor, descarga el Amazon Sales Dataset y colócalo aquí.")
        return

    print("Cargando y limpiando el dataset de Amazon...")
    df_original = pd.read_csv(INPUT_CSV)

    # 2. Seleccionar y renombrar las columnas según el contrato con Edgar
    df_filtrado = df_original[
        ["product_id", "product_name", "about_product"]
    ].copy()
    df_filtrado.columns = ["product_id", "name", "description"]

    # 3. Eliminar filas con valores nulos en columnas críticas
    antes = len(df_filtrado)
    df_filtrado = df_filtrado.dropna(subset=["product_id", "description"])
    despues = len(df_filtrado)

    if antes != despues:
        print(f"Se eliminaron {antes - despues} filas con datos nulos.")

    # Reducir el dataset para pruebas iniciales si lo deseas (ej. primeros 100)
    # df_filtrado = df_filtrado.head(100)

    print(
        "Cargando modelo NLP (all-MiniLM-L6-v2) para vectores de 384 dimensiones..."
    )
    # Este modelo es ideal porque coincide exactamente con el VECTOR(384) de Edgar
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    print("Generando embeddings a partir de 'description'...")
    # Pasamos las descripciones al modelo
    descripciones = df_filtrado["description"].astype(str).tolist()
    vectores_calculados = model.encode(
        descripciones, show_progress_bar=True, batch_size=32
    )

    # 4. Convertir los vectores numéricos a formato texto '[x, y, z...]' limpio para el CSV y pgvector
    print("🔄 Formateando vectores para el almacenamiento limpio...")
    
    # Convertimos cada elemento del vector a un float nativo de Python antes de pasarlo a lista y string
    df_filtrado["embedding"] = [
        str([float(num) for num in v]) for v in vectores_calculados
    ]

    # 5. Guardar el entregable intermedio
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df_filtrado.to_csv(OUTPUT_CSV, index=False)

    print(f"¡Fase 1 Completada con éxito!")
    print(f"Archivo generado con embeddings en: {OUTPUT_CSV}")
    print(f"Total de productos procesados: {len(df_filtrado)}")


if __name__ == "__main__":
    pipeline_generacion_embeddings()