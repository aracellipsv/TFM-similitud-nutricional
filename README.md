# Sistema de Recomendación de Sustituciones Alimentarias

**TFM - Máster en Bioinformática y Bioestadística (UOC)**

## Descripción

Sistema para identificar productos alimentarios nutricionalmente similares dentro de la categoría de cereales, utilizando técnicas de aprendizaje no supervisado. El sistema permite a usuarios y profesionales de la salud encontrar alternativas nutricionales a productos específicos, facilitando decisiones de sustitución informadas.

## Resultados principales

| Métrica | Resultado |
|---------|-----------|
| **Dataset** | 11,601 productos de cereales |
| **Mejor clustering** | HDBSCAN + PCA (Silhouette: 0.556) |
| **Tiempo k-NN** | < 1 ms por consulta |
| **Nutri-Score** | Calculado para 100% de productos |

### Distribución Nutri-Score
- A (más saludable): 16.1%
- B: 15.8%
- C: 43.9%
- D: 19.8%
- E (menos saludable): 4.5%

## Estructura del repositorio

```
TFM-similitud-nutricional/
├── data/
│   ├── raw/                    # Datos crudos de la API USDA
│   │   └── cereales_raw.csv
│   └── processed/              # Datasets procesados
│       ├── cereales_clean.csv
│       ├── cereales_normalized.csv
│       ├── cereales_pca.csv
│       ├── cereales_autoencoder.csv
│       ├── cereales_clustered.csv
│       └── cereales_final.csv
├── docs/                       # Visualizaciones generadas
│   ├── histogramas.png
│   ├── correlaciones.png
│   ├── pca_varianza.png
│   ├── pca_2d.png
│   ├── pca_loadings.png
│   ├── autoencoder_training.png
│   ├── kmeans_elbow.png
│   ├── kmeans_clusters.png
│   ├── dendrograma.png
│   ├── hdbscan_clusters.png
│   ├── comparacion_clustering.png
│   └── nutriscore_distribucion.png
├── notebooks/                  # Jupyter notebooks
│   ├── 01_extraccion_datos.ipynb
│   ├── 02_preprocesamiento_eda.ipynb
│   ├── 03_representaciones.ipynb
│   ├── 04_clustering.ipynb
│   └── 05_sistema_similitud.ipynb
├── src/                        # Modelos guardados
│   ├── scaler.pkl
│   ├── encoder_model.keras
│   ├── knn_normalizado.pkl
│   ├── knn_pca.pkl
│   └── knn_autoencoder.pkl
├── .gitignore
└── README.md
```

## Metodología

### Fase 1: Adquisición y preprocesamiento
- Extracción de datos vía API REST de USDA FoodData Central
- Selección de 8 variables nutricionales: Energía, Proteína, Carbohidratos, Grasas, Grasas saturadas, Fibra, Azúcares, Sodio
- Limpieza de valores faltantes (2.8%) y outliers

### Fase 2: Aprendizaje de representaciones
- **Normalización Z-score**: Estandarización de variables
- **PCA**: Reducción a 5 componentes (91.2% varianza explicada)
- **Autoencoder**: Red neuronal 8→5→3→5→8

### Fase 3: Clustering y similitud
- **K-means**: Método del codo + Silhouette
- **Jerárquico**: Ward linkage con dendrograma
- **HDBSCAN**: Clustering basado en densidad
- **k-NN**: Sistema de búsqueda de productos similares
- **Nutri-Score**: Cálculo para todos los productos

## Tecnologías

- **Python** 3.13
- **Análisis de datos**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, HDBSCAN
- **Deep Learning**: TensorFlow/Keras
- **Visualización**: Matplotlib, Seaborn
- **Entorno**: Miniconda, Jupyter Notebook

## Fuente de datos

[USDA FoodData Central](https://fdc.nal.usda.gov/) - Base de datos Branded Foods

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/aracellipsv/TFM-similitud-nutricional.git
cd TFM-similitud-nutricional

# Crear entorno conda
conda create -n tfm-cereales python=3.13
conda activate tfm-cereales

# Instalar dependencias
pip install pandas numpy scikit-learn hdbscan tensorflow matplotlib seaborn jupyter python-dotenv

# Configurar API key (crear archivo .env)
echo "USDA_API_KEY=tu_api_key_aqui" > .env

# Ejecutar notebooks
jupyter notebook
```

## Uso

```python
# Ejemplo: Buscar productos similares a Cheerios
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import joblib

# Cargar datos y modelo
df = pd.read_csv('data/processed/cereales_final.csv')
knn = joblib.load('src/knn_normalizado.pkl')

# Buscar similares
idx = df[df['description'].str.contains('Cheerios', case=False)].index[0]
distances, indices = knn.kneighbors([X_norm[idx]], n_neighbors=11)

# Mostrar resultados
print(df.iloc[indices[0][1:]]['description'])
```

## Autor

**Aracelli Salinas Venegas**  
Máster en Bioinformática y Bioestadística  
Universitat Oberta de Catalunya (UOC)  
2026

## Tutora

Romina Astrid Rebrij

## Licencia

Este proyecto es parte de un Trabajo Final de Máster académico.
