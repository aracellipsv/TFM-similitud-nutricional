🥣 NutriSim — Sistema de Recomendación de Sustituciones Alimentarias
Trabajo Final de Máster · Bioinformática y Bioestadística · UOC 2026
Autora: Aracelli Salinas Venegas
Tutora: Romina Astrid Rebrij


Descripción
Sistema que, dado un cereal de desayuno comercial, identifica automáticamente los 10 productos nutricionalmente más similares del catálogo y presenta información comparativa —incluyendo el Nutri-Score— para facilitar decisiones de sustitución alimentaria informadas.

El proyecto evalúa de forma sistemática nueve combinaciones de técnicas de representación y agrupamiento sobre 11.608 productos de la base de datos USDA FoodData Central, determinando cuál ofrece la mejor solución de compromiso entre calidad métrica e interpretabilidad nutricional.


Resultados principales
Métrica
Resultado
Dataset
11.608 productos de cereales válidos
Representación final
Normalización z-score (8 variables)
Mejor clustering global
HDBSCAN + PCA (Silhouette: 0,556)
Clustering sistema final
HDBSCAN + Normalizado (Silhouette: 0,542)
Tiempo de respuesta k-NN
< 1 ms por consulta
Nutri-Score calculado
100% del catálogo
Hopkins statistic
H ≥ 0,985 en las 3 representaciones


Hallazgo clave: las métricas cuantitativas de clustering (Silhouette, Hopkins) no garantizan la coherencia alimentaria de las recomendaciones. El autoencoder obtuvo las mejores métricas internas pero generó recomendaciones nutricionalmente incoherentes para productos de perfil moderado. La validación cualitativa mediante casos de uso concretos es imprescindible.


🚀 NutriSim — Interfaz web
La aplicación Streamlit permite buscar cualquier cereal del catálogo y obtener sus 10 sustitutos más similares, con visualización comparativa del perfil nutricional y Nutri-Score.
Requisitos
pip install streamlit pandas numpy scikit-learn joblib plotly
Lanzar la app
cd TFM-similitud-nutricional/src

streamlit run nutrisim_app.py

La app carga automáticamente scaler.pkl, knn_normalizado.pkl y cereales_final.csv desde la misma carpeta src/.
Demo recomendada
Busca "SPECIAL K HOT CEREAL" → selecciona el Cinnamon Raisin (Nutri-Score C) → observa que 8 de las 10 recomendaciones tienen Nutri-Score B.


Estructura del repositorio
TFM-similitud-nutricional/

├── data/

│   ├── raw/

│   │   └── cereales_raw.csv              # Datos crudos de la API USDA

│   └── processed/

│       ├── cereales_clean.csv            # Dataset limpio (11.608 productos)

│       ├── cereales_normalized.csv       # Datos normalizados z-score

│       ├── cereales_pca.csv              # Proyección PCA (5 componentes)

│       ├── cereales_autoencoder.csv      # Espacio latente del autoencoder (3D)

│       ├── cereales_clustered.csv        # Dataset con etiquetas de cluster

│       ├── cereales_final.csv            # Dataset final con Nutri-Score

│       └── resultados_clustering.csv     # Tabla comparativa de 9 configuraciones

├── docs/                                 # Figuras generadas

│   ├── histogramas.png

│   ├── correlaciones.png

│   ├── pca_varianza.png

│   ├── pca_2d.png

│   ├── pca_loadings.png

│   ├── autoencoder_training.png

│   ├── autoencoder_2d.png

│   ├── kmeans_elbow.png

│   ├── kmeans_clusters.png

│   ├── dendrograma.png

│   ├── hdbscan_clusters.png

│   ├── comparacion_clustering.png

│   ├── comparacion_representaciones.png

│   └── nutriscore_distribucion.png

├── notebooks/                            # Análisis completo paso a paso

│   ├── 01_extraccion_datos.ipynb         # Extracción vía API USDA

│   ├── 02_preprocesamiento_eda.ipynb     # Limpieza y análisis exploratorio

│   ├── 03_representaciones.ipynb         # PCA y autoencoder

│   ├── 04_clustering.ipynb              # K-Means, jerárquico, HDBSCAN

│   └── 05_sistema_similitud.ipynb        # k-NN, Nutri-Score y evaluación

├── src/                                  # Modelos entrenados y app

│   ├── nutrisim_app.py                   # Aplicación Streamlit (NutriSim)

│   ├── cereales_final.csv               # Dataset para la app

│   ├── scaler.pkl                        # StandardScaler ajustado

│   ├── knn_normalizado.pkl               # Modelo k-NN (espacio normalizado)

│   ├── knn_pca.pkl                       # Modelo k-NN (espacio PCA)

│   ├── knn_autoencoder.pkl               # Modelo k-NN (espacio autoencoder)

│   └── encoder_model.keras               # Encoder del autoencoder entrenado

├── .gitignore

└── README.md


Metodología
Fase 1 — Datos
Fuente: USDA FoodData Central, sección Branded Foods
Extracción: API REST, consultas paginadas por categoría "Breakfast Cereals"
8 variables nutricionales (por 100 g): energía, proteína, carbohidratos, grasa total, grasa saturada, fibra, azúcares totales, sodio
Preprocesamiento: eliminación de 332 registros con valores faltantes (2,8%) y 55 outliers biológicamente imposibles
Fase 2 — Representaciones comparadas
Representación
Dimensiones
Hopkins
Seleccionada
Normalización z-score
8D
0,985
✅ Sistema final
PCA
5D (91,2% varianza)
0,986
Evaluada
Autoencoder (8→5→3→5→8)
3D
0,989
Evaluada

Fase 3 — Clustering comparado (9 configuraciones)
Algoritmo
Representación
Silhouette
Davies-Bouldin
K-Means k=2
Normalizado
0,340
1,437
K-Means k=2
PCA
0,357
1,317
K-Means k=2
Autoencoder
0,515
0,684
Jerárquico n=5
Normalizado
0,258
1,202
Jerárquico n=5
PCA
0,242
1,407
Jerárquico n=5
Autoencoder
0,375
0,775
HDBSCAN
Normalizado
0,542
0,537
HDBSCAN
PCA
0,556
0,515
HDBSCAN
Autoencoder
0,130
0,998

Fase 4 — Sistema de similitud
Algoritmo: k-NN (k=10 recomendaciones, k=11 internamente)
Métrica: distancia euclidiana en espacio normalizado z-score
Índice: BallTree (scikit-learn)
Tiempo de respuesta: 0,09 ms por consulta


Instalación y reproducción
# Clonar repositorio

git clone https://github.com/aracellipsv/TFM-similitud-nutricional.git

cd TFM-similitud-nutricional

# Crear entorno conda

conda create -n tfm-cereales python=3.13

conda activate tfm-cereales

# Instalar dependencias de análisis

pip install pandas numpy scikit-learn hdbscan tensorflow matplotlib seaborn jupyter python-dotenv

# Configurar clave de API USDA (necesaria solo para re-extraer datos)

echo "USDA_API_KEY=tu_api_key_aqui" > .env

# Ejecutar notebooks en orden

jupyter notebook

Los datos ya están procesados en data/processed/. Solo es necesaria la API key si se desea re-ejecutar el notebook 01_extraccion_datos.ipynb.


Uso del sistema k-NN
import pandas as pd

import joblib

# Cargar datos y modelos

df     = pd.read_csv('src/cereales_final.csv')

scaler = joblib.load('src/scaler.pkl')

knn    = joblib.load('src/knn_normalizado.pkl')

# Variables nutricionales

COLS = ['Energy', 'Protein', 'Carbohydrate, by difference',

        'Total lipid (fat)', 'Fatty acids, total saturated',

        'Fiber, total dietary', 'Total Sugars', 'Sodium, Na']

# Normalizar el dataset

X_norm = scaler.transform(df[COLS].values)

# Buscar los 10 más similares a un producto

producto = df[df['description'].str.contains('SPECIAL K HOT CEREAL CINNAMON', case=False)].iloc[0]

idx = df.index.get_loc(producto.name)

distances, indices = knn.kneighbors([X_norm[idx]], n_neighbors=11)

print(f"Producto: {producto['description']} [{producto['nutriscore_grade']}]\n")

print("Top 10 recomendaciones:")

for i, (dist, rec_idx) in enumerate(zip(distances[0][1:], indices[0][1:]), 1):

    rec = df.iloc[rec_idx]

    print(f"  {i}. [{rec['nutriscore_grade']}] {rec['description']} (d={dist:.3f})")


Tecnologías
Categoría
Herramientas
Lenguaje
Python 3.13
Datos
Pandas, NumPy
Machine Learning
Scikit-learn, HDBSCAN
Deep Learning
TensorFlow/Keras
Visualización
Matplotlib, Seaborn, Plotly
Interfaz web
Streamlit
Entorno
Miniconda, Jupyter Notebook
Control de versiones
Git, GitHub



Fuente de datos
USDA FoodData Central — Base de datos Branded Foods
Acceso programático mediante API REST pública (clave gratuita requerida).


Licencia
Este trabajo está sujeto a una licencia
Reconocimiento-NoComercial-SinObraDerivada 3.0 España (CC BY-NC-ND 3.0)

© 2026 Aracelli Salinas Venegas
