# Sistema de Recomendación de Sustituciones Alimentarias

TFM - Máster en Bioinformática y Bioestadística (UOC)

## Descripción
Sistema para identificar productos alimentarios nutricionalmente similares dentro de la categoría de cereales, utilizando técnicas de aprendizaje no supervisado.

## Estructura
- `data/`: Datos crudos y procesados
- `notebooks/`: Análisis exploratorio y experimentación
- `src/`: Código fuente modular

## Tecnologías
Python 3.10+, Pandas, Scikit-learn, HDBSCAN, TensorFlow/Keras

## Fuente de datos
USDA FoodData Central
```

**.gitignore:**
```
# Datos (no subir archivos grandes)
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep

# Python
__pycache__/
*.pyc
.env
.venv/

# Jupyter
.ipynb_checkpoints/

# IDE
.vscode/
.idea/
