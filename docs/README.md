# Sistema MLOps: Predicción de Cáncer de Mama

## Descripción del Proyecto

Sistema completo de MLOps para la predicción de cáncer de mama utilizando el dataset Breast Cancer Wisconsin. El proyecto implementa un modelo de Machine Learning expuesto como API REST, contenedorizado con Docker y con automatización CI/CD.

## Estructura del Proyecto

```
breast-cancer-mlops/
│
├── data/
│   └── breast_cancer_data.csv
│
├── models/
│   ├── train_model.py
│   └── breast_cancer_model.pkl
│
├── api/
│   ├── app.py
│   └── test_api.py
│
├── tests/
│   └── test_endpoints.py
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── Dockerfile
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

## Requisitos Previos

- Python 3.9 o superior
- Docker
- Git
- Postman (para pruebas de API)

## Instalación Local

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd breast-cancer-mlops
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Entrenar el modelo

```bash
python models/train_model.py
```

### 5. Ejecutar la API localmente

```bash
python api/app.py
```

La API estará disponible en `http://localhost:5000`

## Uso con Docker

### Construir la imagen

```bash
docker build -t breast-cancer-api:latest .
```

### Ejecutar el contenedor

```bash
docker run -p 5000:5000 breast-cancer-api:latest
```

### Verificar contenedor en ejecución

```bash
docker ps
```

## Endpoints de la API

### 1. Health Check

**Endpoint:** `GET /`

**Descripción:** Verifica el estado del servicio

**Respuesta exitosa:**
```json
{
    "status": "ok",
    "message": "Breast Cancer Prediction API is running",
    "version": "1.0.0"
}
```

**Prueba con Postman:**
- Método: GET
- URL: `http://localhost:5000/`
- Headers: No requeridos

### 2. Predicción

**Endpoint:** `POST /predict`

**Descripción:** Realiza predicción de diagnóstico de cáncer de mama

**Request Body (JSON):**
```json
{
    "mean_radius": 17.99,
    "mean_texture": 10.38,
    "mean_perimeter": 122.8,
    "mean_area": 1001.0,
    "mean_smoothness": 0.1184,
    "mean_compactness": 0.2776,
    "mean_concavity": 0.3001,
    "mean_concave_points": 0.1471,
    "mean_symmetry": 0.2419,
    "mean_fractal_dimension": 0.07871,
    "radius_error": 1.095,
    "texture_error": 0.9053,
    "perimeter_error": 8.589,
    "area_error": 153.4,
    "smoothness_error": 0.006399,
    "compactness_error": 0.04904,
    "concavity_error": 0.05373,
    "concave_points_error": 0.01587,
    "symmetry_error": 0.03003,
    "fractal_dimension_error": 0.006193,
    "worst_radius": 25.38,
    "worst_texture": 17.33,
    "worst_perimeter": 184.6,
    "worst_area": 2019.0,
    "worst_smoothness": 0.1622,
    "worst_compactness": 0.6656,
    "worst_concavity": 0.7119,
    "worst_concave_points": 0.2654,
    "worst_symmetry": 0.4601,
    "worst_fractal_dimension": 0.1189
}
```

**Respuesta exitosa:**
```json
{
    "prediction": "M",
    "prediction_label": "Malignant",
    "probability": {
        "Benign": 0.05,
        "Malignant": 0.95
    },
    "confidence": 0.95,
    "timestamp": "2025-09-29T10:30:00"
}
```

**Prueba con Postman:**
- Método: POST
- URL: `http://localhost:5000/predict`
- Headers: `Content-Type: application/json`
- Body: Raw (JSON) con los datos del ejemplo

### Ejemplos de Datos para Pruebas

**Caso Maligno:**
```json
{
    "mean_radius": 20.57,
    "mean_texture": 17.77,
    "mean_perimeter": 132.9,
    "mean_area": 1326.0,
    "mean_smoothness": 0.08474,
    "mean_compactness": 0.07864,
    "mean_concavity": 0.0869,
    "mean_concave_points": 0.07017,
    "mean_symmetry": 0.1812,
    "mean_fractal_dimension": 0.05667,
    "radius_error": 0.5435,
    "texture_error": 0.7339,
    "perimeter_error": 3.398,
    "area_error": 74.08,
    "smoothness_error": 0.005225,
    "compactness_error": 0.01308,
    "concavity_error": 0.0186,
    "concave_points_error": 0.0134,
    "symmetry_error": 0.01389,
    "fractal_dimension_error": 0.003532,
    "worst_radius": 24.99,
    "worst_texture": 23.41,
    "worst_perimeter": 158.8,
    "worst_area": 1956.0,
    "worst_smoothness": 0.1238,
    "worst_compactness": 0.1866,
    "worst_concavity": 0.2416,
    "worst_concave_points": 0.186,
    "worst_symmetry": 0.275,
    "worst_fractal_dimension": 0.08902
}
```

**Caso Benigno:**
```json
{
    "mean_radius": 13.54,
    "mean_texture": 14.36,
    "mean_perimeter": 87.46,
    "mean_area": 566.3,
    "mean_smoothness": 0.09779,
    "mean_compactness": 0.08129,
    "mean_concavity": 0.06664,
    "mean_concave_points": 0.04781,
    "mean_symmetry": 0.1885,
    "mean_fractal_dimension": 0.05766,
    "radius_error": 0.2699,
    "texture_error": 0.7886,
    "perimeter_error": 2.058,
    "area_error": 23.56,
    "smoothness_error": 0.008462,
    "compactness_error": 0.0146,
    "concavity_error": 0.02387,
    "concave_points_error": 0.01315,
    "symmetry_error": 0.0198,
    "fractal_dimension_error": 0.0023,
    "worst_radius": 15.11,
    "worst_texture": 19.26,
    "worst_perimeter": 99.7,
    "worst_area": 711.2,
    "worst_smoothness": 0.144,
    "worst_compactness": 0.1773,
    "worst_concavity": 0.239,
    "worst_concave_points": 0.1288,
    "worst_symmetry": 0.2977,
    "worst_fractal_dimension": 0.07259
}
```

## Manejo de Errores

### Error 400 - Datos Inválidos

```json
{
    "error": "Invalid input",
    "message": "Missing required fields: ['mean_radius', 'mean_texture']"
}
```

### Error 500 - Error del Servidor

```json
{
    "error": "Prediction failed",
    "message": "Internal server error description"
}
```

## CI/CD con GitHub Actions

El proyecto incluye un workflow automatizado que:

1. Ejecuta tests unitarios
2. Construye la imagen Docker
3. Ejecuta tests de integración
4. Publica la imagen en Docker Hub (opcional)

El workflow se activa automáticamente con cada push a las ramas main o develop.

## Modelo de Machine Learning

### Características del Modelo

- **Algoritmo:** Random Forest Classifier
- **Features:** 30 características numéricas del dataset Breast Cancer Wisconsin
- **Clases:** B (Benigno), M (Maligno)
- **Métricas de Evaluación:**
  - Accuracy: ~96%
  - Precision: ~95%
  - Recall: ~94%
  - F1-Score: ~95%

### Proceso de Entrenamiento

El modelo fue entrenado siguiendo estos pasos:

1. Carga del dataset desde sklearn
2. División train/test (80/20)
3. Estandarización de features con StandardScaler
4. Entrenamiento con Random Forest (100 estimadores)
5. Validación cruzada
6. Serialización con joblib

## Buenas Prácticas Implementadas

### Código

- Cumplimiento de PEP 8
- Type hints en funciones
- Docstrings en módulos y funciones
- Separación de responsabilidades
- Manejo robusto de excepciones
- Logging estructurado

### Docker

- Imagen base ligera (python:3.9-slim)
- Multi-stage builds (no aplicado por simplicidad)
- .dockerignore para reducir contexto
- Variables de entorno configurables
- Health checks del contenedor

### Seguridad

- Validación de entradas
- Sanitización de datos
- Logs sin información sensible
- Usuario no privilegiado en Docker

## Testing

### Ejecutar tests locales

```bash
pytest tests/ -v
```

### Ejecutar tests de cobertura

```bash
pytest tests/ --cov=api --cov-report=html
```

## Monitoreo y Logs

Los logs se generan en formato estructurado con niveles:

- INFO: Operaciones normales
- WARNING: Situaciones de atención
- ERROR: Errores capturados
- DEBUG: Información detallada (desarrollo)

## Troubleshooting

### El contenedor no inicia

```bash
docker logs <container_id>
```

### La API no responde

Verificar que el puerto 5000 no esté en uso:

```bash
# Linux/Mac
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

### Error al cargar el modelo

Verificar que el archivo `models/breast_cancer_model.pkl` existe y ejecutar:

```bash
python models/train_model.py
```

## Mejoras Futuras

- Implementar autenticación JWT
- Agregar rate limiting
- Monitoreo con Prometheus y Grafana
- Deploy en servicios cloud (AWS, GCP, Azure)
- Implementar A/B testing de modelos
- Agregar versionado de modelos
- Dashboard de métricas en tiempo real


## Referencias

- Dataset: [Breast Cancer Wisconsin](https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data)
- Documentación Flask: https://flask.palletsprojects.com/
- Docker: https://docs.docker.com/
- GitHub Actions: https://docs.github.com/actions