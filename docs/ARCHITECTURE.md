# Arquitectura del Sistema

## Sistema MLOps: Predicción de Cáncer de Mama

---

## 1. Visión General

El sistema implementa una arquitectura de microservicios para exponer un modelo de Machine Learning mediante una API REST, contenedorizado con Docker y con flujo automatizado de CI/CD.

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        Cliente                               │
│                     (Postman/Browser)                        │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/JSON
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Docker Container                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Flask API (Port 5000)                    │  │
│  │                                                       │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐ │  │
│  │  │  GET /      │  │ POST /predict│  │ GET /features│ │  │
│  │  │ Health Check│  │  Prediction  │  │   Feature   │ │  │
│  │  └─────────────┘  └──────────────┘  └─────────────┘ │  │
│  │         │                │                  │        │  │
│  │         └────────────────┼──────────────────┘        │  │
│  │                          ▼                           │  │
│  │              ┌─────────────────────┐                 │  │
│  │              │  ModelPredictor     │                 │  │
│  │              │  - validate_input() │                 │  │
│  │              │  - predict()        │                 │  │
│  │              └──────────┬──────────┘                 │  │
│  │                         │                            │  │
│  │                         ▼                            │  │
│  │         ┌───────────────────────────────┐           │  │
│  │         │     Serialized Models         │           │  │
│  │         │  - breast_cancer_model.pkl    │           │  │
│  │         │  - scaler.pkl                 │           │  │
│  │         │  - model_metadata.pkl         │           │  │
│  │         └───────────────────────────────┘           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              GitHub Actions (CI/CD)                   │  │
│  │                                                       │  │
│  │  Push/PR  →  Build  →  Test  →  Docker  →  Deploy   │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes del Sistema

### 2.1 Módulo de Entrenamiento (`models/train_model.py`)

**Responsabilidad:** Entrenar y serializar el modelo de Machine Learning.

**Características:**

- Carga del dataset Breast Cancer Wisconsin desde sklearn
- Preprocesamiento y normalización de datos
- Entrenamiento de Random Forest Classifier
- Validación cruzada y evaluación de métricas
- Serialización del modelo, scaler y metadata

**Clase Principal:**

```python
BreastCancerModelTrainer
├── load_data()
├── preprocess_data()
├── train_model()
├── evaluate_model()
└── save_model()
```

### 2.2 API REST (`api/app.py`)

**Responsabilidad:** Exponer el modelo como servicio REST.

**Endpoints:**

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | / | Health check del servicio |
| POST | /predict | Realizar predicción |
| GET | /features | Obtener lista de features |

**Clase Principal:**

```python
ModelPredictor
├── load_model()
├── validate_input()
└── predict()
```

**Características de Seguridad:**

- Validación estricta de entradas
- Manejo robusto de excepciones
- Logging estructurado
- Sanitización de datos

### 2.3 Testing (`tests/test_endpoints.py`)

**Responsabilidad:** Garantizar calidad y funcionalidad del código.

**Tipos de Tests:**

- Tests unitarios de cada endpoint
- Tests de validación de entrada
- Tests de manejo de errores
- Tests de integración

**Cobertura esperada:** 85%+

### 2.4 Contenedor Docker

**Responsabilidad:** Encapsular la aplicación en un entorno reproducible.

**Características:**

- Imagen base: `python:3.9-slim`
- Usuario no privilegiado para seguridad
- Health checks integrados
- Optimización de capas

### 2.5 CI/CD Pipeline

**Responsabilidad:** Automatizar el flujo de desarrollo y despliegue.

**Stages:**

1. **Test:** Ejecutar tests y validar código
2. **Build:** Construir imagen Docker
3. **Integration Test:** Validar imagen Docker
4. **Deploy:** Publicar imagen (opcional)

---

## 3. Decisiones Técnicas

### 3.1 Selección del Modelo

**Decisión:** Random Forest Classifier

**Justificación:**

- Alta precisión para clasificación binaria
- Robusto ante overfitting
- No requiere escalado estricto de features
- Interpretabilidad mediante feature importance
- Rápido en predicción

**Alternativas Consideradas:**

- Logistic Regression: Menos preciso en este dataset
- SVM: Mayor tiempo de entrenamiento
- Neural Networks: Overkill para este problema
- XGBoost: Similar performance pero más complejo

**Hiperparámetros Seleccionados:**

```python
RandomForestClassifier(
    n_estimators=100,      # Balance entre performance y tiempo
    max_depth=10,          # Prevenir overfitting
    min_samples_split=5,   # Generalización
    min_samples_leaf=2,    # Estabilidad
    random_state=42,       # Reproducibilidad
    n_jobs=-1              # Paralelización
)
```

### 3.2 Framework API: Flask

**Decisión:** Flask para la API REST

**Justificación:**

- Ligero y minimalista
- Fácil de entender y mantener
- Excelente documentación
- Gran ecosistema de extensiones
- Adecuado para microservicios

**Alternativas Consideradas:**

- FastAPI: Más moderno pero menos maduro
- Django REST: Demasiado pesado para este caso
- Flask-RESTful: Añade complejidad innecesaria

### 3.3 Serialización del Modelo

**Decisión:** joblib para serialización

**Justificación:**

- Optimizado para objetos numpy grandes
- Más eficiente que pickle para modelos sklearn
- Ampliamente usado en producción
- Compatible con versionado

**Formato:**

```python
joblib.dump(model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(metadata, 'metadata.pkl')
```

### 3.4 Validación de Entrada

**Decisión:** Validación manual en lugar de frameworks

**Justificación:**

- Control total sobre el proceso
- Mensajes de error personalizados
- Sin dependencias adicionales
- Mejor performance

**Proceso de Validación:**

1. Verificar Content-Type
2. Verificar body no vacío
3. Verificar presencia de todas las features
4. Verificar tipos de datos numéricos
5. Transformar datos al formato esperado

### 3.5 Contenedorización

**Decisión:** Docker con imagen slim

**Justificación:**

- Entorno reproducible
- Aislamiento de dependencias
- Fácil despliegue
- Imagen slim reduce tamaño

**Optimizaciones:**

- Multi-stage no aplicado (simplicidad)
- Usuario no root (seguridad)
- .dockerignore optimizado
- Health checks integrados

### 3.6 CI/CD: GitHub Actions

**Decisión:** GitHub Actions para CI/CD

**Justificación:**

- Integración nativa con GitHub
- Gratuito para repositorios públicos
- Configuración declarativa con YAML
- Gran marketplace de actions

**Alternativas Consideradas:**

- GitLab CI: Requiere GitLab
- Jenkins: Demasiado complejo para este proyecto
- CircleCI: Requiere configuración externa

---

## 4. Flujo de Datos

### 4.1 Flujo de Entrenamiento

```
Dataset (sklearn)
    ↓
Load & Explore
    ↓
Train/Test Split (80/20)
    ↓
Feature Scaling (StandardScaler)
    ↓
Model Training (Random Forest)
    ↓
Cross-Validation (5-fold)
    ↓
Evaluation & Metrics
    ↓
Serialization (joblib)
    ↓
Model Files (.pkl)
```

### 4.2 Flujo de Predicción

```
HTTP Request (JSON)
    ↓
Validation Layer
    ↓
Feature Extraction
    ↓
Feature Scaling (saved scaler)
    ↓
Model Prediction
    ↓
Probability Calculation
    ↓
Response Formatting
    ↓
HTTP Response (JSON)
```

### 4.3 Flujo CI/CD

```
Git Push/PR
    ↓
GitHub Actions Trigger
    ↓
┌────────────────────┐
│  Stage 1: Test     │
│  - Install deps    │
│  - Train model     │
│  - Run pytest      │
└────────┬───────────┘
         ↓
┌────────────────────┐
│  Stage 2: Build    │
│  - Build Docker    │
│  - Tag image       │
└────────┬───────────┘
         ↓
┌────────────────────┐
│  Stage 3: Test     │
│  - Run container   │
│  - Integration test│
└────────┬───────────┘
         ↓
┌────────────────────┐
│  Stage 4: Deploy   │
│  - Push to registry│ (opcional)
└────────────────────┘
```

---

## 5. Seguridad

### 5.1 Medidas Implementadas

**A nivel de API:**

- Validación estricta de entradas
- Sanitización de datos
- Manejo de errores sin exponer internos
- Logging sin información sensible
- Rate limiting (pendiente)

**A nivel de Docker:**

- Usuario no privilegiado (apiuser)
- Sin credenciales hardcodeadas
- Minimal base image
- Health checks

**A nivel de Código:**

- Sin secretos en el código
- Variables de entorno para configuración
- Dependencias con versiones fijas

### 5.2 Mejoras de Seguridad Futuras

- Implementar autenticación JWT
- HTTPS/TLS
- Rate limiting
- Input sanitization más robusta
- Monitoreo de anomalías
- Auditoría de accesos

---

## 6. Escalabilidad

### 6.1 Diseño Actual

**Limitaciones:**

- Single-threaded Flask (desarrollo)
- Sin balanceo de carga
- Sin caché de predicciones
- Sin persistencia de estado

**Capacidad Estimada:**

- ~50 requests/segundo (local)
- Latencia promedio: 50-100ms

### 6.2 Estrategias de Escalado

**Horizontal:**

```
Load Balancer (nginx)
    ↓
┌─────────┬─────────┬─────────┐
│ API 1   │ API 2   │ API 3   │
└─────────┴─────────┴─────────┘
```

**Vertical:**

- Usar servidor WSGI (Gunicorn)
- Aumentar workers
- Optimizar hiperparámetros

**Caché:**

- Redis para predicciones frecuentes
- Cache de features normalizadas

---

## 7. Monitoreo y Observabilidad

### 7.1 Logging

**Niveles Implementados:**

- INFO: Operaciones normales
- WARNING: Situaciones de atención
- ERROR: Errores capturados

**Formato:**

```
timestamp - module - level - message
```

### 7.2 Métricas Recomendadas

**Métricas de Negocio:**

- Número de predicciones/día
- Distribución de predicciones (M vs B)
- Confianza promedio

**Métricas Técnicas:**

- Latencia de predicción
- Tasa de errores
- Uso de CPU/Memoria
- Throughput

**Herramientas Sugeridas:**

- Prometheus para métricas
- Grafana para visualización
- ELK Stack para logs

---

## 8. Mantenimiento del Modelo

### 8.1 Model Drift

**Consideraciones:**

- El modelo puede degradarse con el tiempo
- Distribución de datos puede cambiar
- Nuevas features pueden ser relevantes

**Estrategias:**

1. Monitorear accuracy en producción
2. Comparar distribución de predicciones
3. Reentrenar periódicamente
4. A/B testing de nuevas versiones

### 8.2 Versionado

**Sistema Recomendado:**

```
models/
  ├── v1.0.0/
  │   ├── model.pkl
  │   ├── scaler.pkl
  │   └── metadata.json
  ├── v1.1.0/
  │   └── ...
  └── production -> v1.0.0/
```

---

## 9. Calidad del Código

### 9.1 Estándares

**PEP 8:**

- Indentación: 4 espacios
- Líneas: máximo 79 caracteres
- Docstrings: Google style
- Type hints donde sea apropiado

**Estructura:**

```python
"""Module docstring."""

import standard_library
import third_party
import local_modules


class MyClass:
    """Class docstring."""
    
    def method(self, arg: str) -> dict:
        """Method docstring."""
        pass
```

### 9.2 Testing

**Cobertura:**

- Objetivo: 85%+
- Tests unitarios: 70%
- Tests de integración: 15%

**Estrategia:**

- Test-Driven Development (TDD) recomendado
- Tests automáticos en CI/CD
- Mock de dependencias externas

---

## 10. Documentación

### 10.1 Niveles de Documentación

**Código:**

- Docstrings en todos los módulos
- Comments para lógica compleja
- Type hints

**API:**

- README.md general
- POSTMAN_GUIDE.md para uso
- Ejemplos de requests/responses

**Arquitectura:**

- Este documento (ARCHITECTURE.md)
- Diagramas actualizados
- Decisiones técnicas documentadas

### 10.2 Mantenimiento

La documentación debe actualizarse:

- Con cada cambio significativo
- Antes de cada release
- Cuando se agregan features
- Cuando se deprecan funcionalidades

---

## 11. Referencias

**Tecnologías:**

- Flask: https://flask.palletsprojects.com/
- scikit-learn: https://scikit-learn.org/
- Docker: https://docs.docker.com/
- GitHub Actions: https://docs.github.com/actions

**Buenas Prácticas:**

- 12 Factor App: https://12factor.net/
- MLOps Principles: https://ml-ops.org/
- API Design: https://restfulapi.net/

**Dataset:**

- Breast Cancer Wisconsin: https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)