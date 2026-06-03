# 🥣 NutriSim — Nutritional Similarity Recommendation System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-app-FF4B4B?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/TensorFlow-Autoencoder-FF6F00?logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/License-CC%20BY--NC--ND%203.0-lightgrey" />
</p>

<p align="center">
  <strong>Trabajo Final de Máster · Bioinformática y Bioestadística · UOC 2026</strong><br>
  Aracelli Salinas Venegas · Tutora: Romina Astrid Rebrij
</p>

---

## ¿Qué hace este proyecto?

Dado un cereal de desayuno comercial, el sistema identifica automáticamente los **10 productos nutricionalmente más similares** del catálogo USDA y presenta información comparativa —incluyendo el Nutri-Score— para facilitar decisiones de sustitución alimentaria informadas.

El proyecto compara sistemáticamente **9 combinaciones** de técnicas de representación y agrupamiento sobre 11.608 productos, determinando cuál ofrece el mejor equilibrio entre calidad métrica e interpretabilidad nutricional.

> **Hallazgo central:** las métricas cuantitativas de clustering (Silhouette, Hopkins) no garantizan la coherencia alimentaria de las recomendaciones. El autoencoder obtuvo las mejores métricas pero generó sustitutos nutricionalmente incoherentes, evidenciando la necesidad imprescindible de validación cualitativa.

---

## 🚀 Lanzar NutriSim

```bash
# Instalar dependencias
pip install streamlit pandas numpy scikit-learn joblib plotly

# Ejecutar desde la carpeta src/
cd src
streamlit run nutrisim_app.py
```

**Demo recomendada:** busca `SPECIAL K HOT CEREAL` → selecciona Cinnamon Raisin (Nutri-Score C) → observa que 8 de las 10 recomendaciones tienen Nutri-Score B.

---

## 📊 Resultados principales

| Métrica | Resultado |
|---|---|
| Dataset final | **11.608 productos** de cereales USDA |
| Representación seleccionada | Normalización z-score (8 variables) |
| Mejor clustering global | HDBSCAN + PCA · Silhouette = **0,556** |
| Clustering sistema final | HDBSCAN + Normalizado · Silhouette = **0,542** |
| Tiempo de respuesta k-NN | **< 1 ms** por consulta |
| Nutri-Score calculado | **100%** del catálogo |
| Tendencia al agrupamiento | Hopkins H ≥ **0,985** en las 3 representaciones |

### Comparación de las 9 configuraciones

| Algoritmo | Representación | Silhouette | Davies-Bouldin |
|---|---|:---:|:---:|
| K-Means k=2 | Normalizado | 0,340 | 1,437 |
| K-Means k=2 | PCA | 0,357 | 1,317 |
| K-Means k=2 | Autoencoder | 0,515 | 0,684 |
| Jerárquico n=5 | Normalizado | 0,258 | 1,202 |
| Jerárquico n=5 | PCA | 0,242 | 1,407 |
| Jerárquico n=5 | Autoencoder | 0,375 | 0,775 |
| **HDBSCAN** ✅ | **Normalizado** | **0,542** | **0,537** |
| HDBSCAN | PCA | 0,556 | 0,515 |
| HDBSCAN | Autoencoder | 0,130 | 0,998 |

---

## 🗂️ Estructura del repositorio

```
TFM-similitud-nutricional/
│
├── 📓 notebooks/
│   ├── 01_extraccion_datos.ipynb         # Extracción vía API USDA
│   ├── 02_preprocesamiento_eda.ipynb     # Limpieza y análisis exploratorio
│   ├── 03_representaciones.ipynb         # PCA y autoencoder
│   ├── 04_clustering.ipynb               # K-Means, jerárquico, HDBSCAN
│   └── 05_sistema_similitud.ipynb        # k-NN, Nutri-Score y evaluación
│
├── 🗃️ data/
│   ├── raw/cereales_raw.csv              # Datos crudos de la API USDA
│   └── processed/
│       ├── cereales_clean.csv            # Dataset limpio (11.608 productos)
│       ├── cereales_normalized.csv       # Datos normalizados z-score
│       ├── cereales_pca.csv              # Proyección PCA (5 componentes)
│       ├── cereales_autoencoder.csv      # Espacio latente autoencoder (3D)
│       ├── cereales_final.csv            # Dataset con Nutri-Score calculado
│       └── resultados_clustering.csv     # Tabla comparativa 9 configuraciones
│
├── 🤖 src/
│   ├── nutrisim_app.py                   # Aplicación Streamlit
│   ├── cereales_final.csv                # Dataset para la app
│   ├── scaler.pkl                        # StandardScaler ajustado
│   ├── knn_normalizado.pkl               # Modelo k-NN (espacio normalizado) ✅
│   ├── knn_pca.pkl                       # Modelo k-NN (espacio PCA)
│   ├── knn_autoencoder.pkl               # Modelo k-NN (espacio autoencoder)
│   └── encoder_model.keras               # Encoder del autoencoder entrenado
│
└── 📈 docs/                              # Figuras y visualizaciones generadas
```

---

## ⚙️ Instalación y reproducción

```bash
git clone https://github.com/aracellipsv/TFM-similitud-nutricional.git
cd TFM-similitud-nutricional

conda create -n tfm-cereales python=3.13
conda activate tfm-cereales

pip install pandas numpy scikit-learn hdbscan tensorflow matplotlib seaborn jupyter python-dotenv

# Solo si se desea re-extraer datos desde la API
echo "USDA_API_KEY=tu_api_key_aqui" > .env

jupyter notebook
```

> Los datos ya están procesados en `data/processed/`. Los notebooks se ejecutan en orden del 01 al 05.

---

## 💻 Uso del sistema k-NN

```python
import pandas as pd, joblib

df     = pd.read_csv('src/cereales_final.csv')
scaler = joblib.load('src/scaler.pkl')
knn    = joblib.load('src/knn_normalizado.pkl')

COLS = ['Energy', 'Protein', 'Carbohydrate, by difference', 'Total lipid (fat)',
        'Fatty acids, total saturated', 'Fiber, total dietary', 'Total Sugars', 'Sodium, Na']

X_norm = scaler.transform(df[COLS].values)

# Buscar los 10 más similares a un producto
producto = df[df['description'].str.contains('SPECIAL K HOT CEREAL CINNAMON', case=False)].iloc[0]
idx = df.index.get_loc(producto.name)

distances, indices = knn.kneighbors([X_norm[idx]], n_neighbors=11)

print(f"Producto: {producto['description']} [{producto['nutriscore_grade']}]\n")
for i, (dist, rec_idx) in enumerate(zip(distances[0][1:], indices[0][1:]), 1):
    rec = df.iloc[rec_idx]
    print(f"  {i}. [{rec['nutriscore_grade']}] {rec['description']} (d={dist:.3f})")
```

---

## 🛠️ Tecnologías

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.x-F7931E?logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?logo=tensorflow&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)

---

## 📄 Licencia

Este trabajo está sujeto a una licencia
[CC BY-NC-ND 3.0 España](http://creativecommons.org/licenses/by-nc-nd/3.0/es/) · © 2026 Aracelli Salinas Venegas