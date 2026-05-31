# Proyecto de Base de Datos Vectorial - Grupo 4

## Integrantes:
* **Apaza Vilca Tania Pamela** 
* **Avila Agramonte Edgar** 
* **Condori Gutierrez Rodrigo Bernardo** 
* **Mamani Humpiri Isaac Joel** 
* **Ramos Vargas Jaqueline Rocio** 

Este proyecto implementa un sistema de **búsqueda semántica y recomendación de productos** de e-commerce utilizando **PostgreSQL** como base de datos vectorial mediante la extensión **pgvector**, un backend en **FastAPI** y un micro frontend.

El pipeline procesa un dataset real de Amazon, convirtiendo las descripciones de los productos en embeddings vectoriales de 384 dimensiones para permitir búsquedas por significado y contexto, y no solo por palabras clave exactas.

---

## 🛠️ Arquitectura del Repositorio

```text
📂 Trabajo grupal/
├── 📄 docker-compose.yml        # Orquesta la base de datos y el contenedor de carga
├── 📄 Dockerfile                # Entorno aislado para ejecutar el pipeline de Python
├── 📂 init-scripts/
│   └── 📄 init.sql               # Inicialización automática de la base de datos (pgvector y tablas)
├── 📂 ml-artifacts/
│   └── 📂 embeddings/
│       └── 📄 item_embeddings.csv     # Entregable: Dataset de Amazon con Embeddings (1,351 productos)
├── 📄 generar_embeddings.py       # Respaldo de IA: Modelo NLP SentenceTransformers
└── 📄 cargar_en_postgres.py       # Código ETL: Lógica de inserción masiva por lotes
```

--- 
# Guía de Inicialización y Carga de Datos

## 1. Desplegar el Entorno Global

```bash
docker compose up -d
```

## 2. Poblar la Base de Datos Vectorial

Ejecuta el pipeline ETL para leer el archivo CSV e insertar masivamente los **1,351 productos** junto con sus respectivos vectores en PostgreSQL:

```bash
python cargar_en_postgres.py
```

---

# 🔍 Verificación Definitiva de los Datos

Para comprobar visualmente que la base de datos se cargó correctamente y que las columnas mantienen el formato esperado del proyecto, ejecuta la siguiente consulta directamente sobre el contenedor:

```bash
docker exec -i postgres_vector_db psql -U postgres -d ecommerce_vectorial -c "
SELECT 
    product_id, 
    LEFT(name, 45) || '...' as name, 
    LEFT(description, 50) || '...' as description, 
    LEFT(embedding::text, 45) || '...' as embedding
FROM products 
LIMIT 3;
"
```

### Resultado esperado

La consulta debería mostrar:

- El identificador del producto (`product_id`).
- Una vista truncada del nombre (`name`).
- Una vista truncada de la descripción (`description`).
- Una vista truncada del vector almacenado en la columna `embedding`.

Si se muestran registros correctamente, la carga de datos en PostgreSQL con **pgvector** se realizó con éxito.
