# Guía de Pruebas con Postman

Esta guía detalla cómo probar la API de predicción de cáncer de mama usando Postman.

## Requisitos Previos

1. Tener Postman instalado (descargar de https://www.postman.com/downloads/)
2. La API debe estar ejecutándose (local o Docker)
3. URL base: `http://localhost:5000`

## Configuración Inicial de Postman

### Crear una Colección

1. Abrir Postman
2. Click en "Collections" en el panel izquierdo
3. Click en el botón "+" o "New Collection"
4. Nombrar la colección: "Breast Cancer Prediction API"
5. Agregar descripción: "Colección de pruebas para la API de predicción de cáncer de mama"

### Configurar Variables de Entorno (Opcional)

1. Click en el icono de engranaje (Settings)
2. Click en "Add" para crear un nuevo entorno
3. Nombre: "Local Development"
4. Agregar variable:
   - Variable: `base_url`
   - Initial Value: `http://localhost:5000`
   - Current Value: `http://localhost:5000`
5. Click "Add" y seleccionar el entorno

## Pruebas de Endpoints

### 1. Health Check (GET /)

**Propósito:** Verificar que el servicio está funcionando correctamente.

**Configuración en Postman:**

1. Click en "Add Request" dentro de la colección
2. Nombre: "Health Check"
3. Método: `GET`
4. URL: `{{base_url}}/` o `http://localhost:5000/`
5. Headers: No requeridos
6. Click "Send"

**Respuesta Esperada (200 OK):**

```json
{
    "status": "ok",
    "message": "Breast Cancer Prediction API is running",
    "version": "1.0.0",
    "model_info": {
        "type": "RandomForestClassifier",
        "training_date": "2025-09-29T10:00:00.000000",
        "features_count": 30
    },
    "timestamp": "2025-09-29T10:30:00.000000"
}
```

**Tests Automáticos (Pestaña Tests en Postman):**

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has status ok", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.status).to.eql("ok");
});

pm.test("Response has version", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.version).to.exist;
});
```

### 2. Obtener Features Requeridas (GET /features)

**Propósito:** Obtener la lista de todas las features necesarias para hacer predicciones.

**Configuración en Postman:**

1. Nuevo Request: "Get Features"
2. Método: `GET`
3. URL: `{{base_url}}/features`
4. Click "Send"

**Respuesta Esperada (200 OK):**

```json
{
    "features": [
        "mean_radius",
        "mean_texture",
        "mean_perimeter",
        "mean_area",
        "mean_smoothness",
        "mean_compactness",
        "mean_concavity",
        "mean_concave_points",
        "mean_symmetry",
        "mean_fractal_dimension",
        "radius_error",
        "texture_error",
        "perimeter_error",
        "area_error",
        "smoothness_error",
        "compactness_error",
        "concavity_error",
        "concave_points_error",
        "symmetry_error",
        "fractal_dimension_error",
        "worst_radius",
        "worst_texture",
        "worst_perimeter",
        "worst_area",
        "worst_smoothness",
        "worst_compactness",
        "worst_concavity",
        "worst_concave_points",
        "worst_symmetry",
        "worst_fractal_dimension"
    ],
    "count": 30,
    "description": "Lista de features requeridas para predicción"
}
```

**Tests Automáticos:**

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Returns 30 features", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.count).to.eql(30);
    pm.expect(jsonData.features).to.have.lengthOf(30);
});
```

### 3. Predicción - Caso Maligno (POST /predict)

**Propósito:** Realizar una predicción con datos de un caso maligno.

**Configuración en Postman:**

1. Nuevo Request: "Predict - Malignant Case"
2. Método: `POST`
3. URL: `{{base_url}}/predict`
4. Headers:
   - Key: `Content-Type`
   - Value: `application/json`
5. Body > Raw > JSON:

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

6. Click "Send"

**Respuesta Esperada (200 OK):**

```json
{
    "prediction": 0,
    "prediction_label": "Malignant",
    "probability": {
        "Malignant": 0.95,
        "Benign": 0.05
    },
    "confidence": 0.95,
    "timestamp": "2025-09-29T10:30:00.000000"
}
```

**Tests Automáticos:**

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains prediction", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.prediction).to.exist;
    pm.expect(jsonData.prediction_label).to.exist;
});

pm.test("Probability object exists", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.probability).to.be.an('object');
    pm.expect(jsonData.probability.Malignant).to.exist;
    pm.expect(jsonData.probability.Benign).to.exist;
});

pm.test("Confidence is between 0 and 1", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.confidence).to.be.at.least(0);
    pm.expect(jsonData.confidence).to.be.at.most(1);
});
```

### 4. Predicción - Caso Benigno (POST /predict)

**Propósito:** Realizar una predicción con datos de un caso benigno.

**Configuración en Postman:**

1. Nuevo Request: "Predict - Benign Case"
2. Método: `POST`
3. URL: `{{base_url}}/predict`
4. Headers: `Content-Type: application/json`
5. Body > Raw > JSON:

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

**Respuesta Esperada (200 OK):**

```json
{
    "prediction": 1,
    "prediction_label": "Benign",
    "probability": {
        "Malignant": 0.10,
        "Benign": 0.90
    },
    "confidence": 0.90,
    "timestamp": "2025-09-29T10:30:00.000000"
}
```

### 5. Error - Features Faltantes (POST /predict)

**Propósito:** Verificar el manejo de errores cuando faltan features.

**Configuración en Postman:**

1. Nuevo Request: "Error - Missing Features"
2. Método: `POST`
3. URL: `{{base_url}}/predict`
4. Headers: `Content-Type: application/json`
5. Body > Raw > JSON:

```json
{
    "mean_radius": 20.57,
    "mean_texture": 17.77
}
```

**Respuesta Esperada (400 Bad Request):**

```json
{
    "error": "Invalid input",
    "message": "Faltan features requeridas o valores inválidos",
    "missing_features": [
        "mean_perimeter",
        "mean_area",
        "..."
    ],
    "required_features": ["..."]
}
```

**Tests Automáticos:**

```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Error message exists", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.error).to.eql("Invalid input");
});
```

### 6. Error - Body Vacío (POST /predict)

**Propósito:** Verificar el manejo de errores con body vacío.

**Configuración en Postman:**

1. Nuevo Request: "Error - Empty Body"
2. Método: `POST`
3. URL: `{{base_url}}/predict`
4. Headers: `Content-Type: application/json`
5. Body > Raw > JSON:

```json
{}
```

**Respuesta Esperada (400 Bad Request):**

```json
{
    "error": "Empty request",
    "message": "El body no puede estar vacío"
}
```

### 7. Error - Content-Type Inválido (POST /predict)

**Propósito:** Verificar el manejo de errores con Content-Type incorrecto.

**Configuración en Postman:**

1. Nuevo Request: "Error - Invalid Content Type"
2. Método: `POST`
3. URL: `{{base_url}}/predict`
4. Headers: `Content-Type: text/plain`
5. Body > Raw: `invalid data`

**Respuesta Esperada (400 Bad Request):**

```json
{
    "error": "Invalid content type",
    "message": "Content-Type debe ser application/json"
}
```

### 8. Error - Valores No Numéricos (POST /predict)

**Propósito:** Verificar validación de tipos de datos.

**Configuración en Postman:**

1. Nuevo Request: "Error - Invalid Data Types"
2. Método: `POST`
3. URL: `{{base_url}}/predict`
4. Headers: `Content-Type: application/json`
5. Body con al menos un valor no numérico:

```json
{
    "mean_radius": "not_a_number",
    "mean_texture": 17.77,
    "..."
}
```

**Respuesta Esperada (400 Bad Request).**

## Suite de Tests Completa

### Crear Collection Runner

1. Click en la colección "Breast Cancer Prediction API"
2. Click en "Run"
3. Seleccionar todos los requests
4. Click "Run Breast Cancer Prediction API"
5. Ver resultados de todas las pruebas

### Exportar Colección

1. Click derecho en la colección
2. "Export"
3. Formato: Collection v2.1 (recommended)
4. Guardar archivo JSON

### Importar Colección

1. Click "Import" en Postman
2. Seleccionar archivo JSON exportado
3. Click "Import"

## Tests Avanzados con Pre-request Scripts

### Generar Datos Aleatorios

En la pestaña "Pre-request Script" de un request:

```javascript
// Generar valores aleatorios para testing
pm.environment.set("random_radius", Math.random() * 30 + 5);
pm.environment.set("random_texture", Math.random() * 40 + 5);
// Agregar más según necesidad
```

Luego usar en el Body:

```json
{
    "mean_radius": {{random_radius}},
    "mean_texture": {{random_texture}},
    "..."
}
```

## Monitoreo y Automatización

### Monitor en Postman (Opcional)

1. Click en la colección
2. Click en "..." > "Monitor collection"
3. Configurar frecuencia de ejecución
4. Agregar notificaciones por email

### Newman (CLI)

Para ejecutar tests desde terminal:

```bash
# Instalar Newman
npm install -g newman

# Ejecutar colección
newman run breast-cancer-api-collection.json -e local-environment.json

# Con reportes
newman run breast-cancer-api-collection.json -r html,cli
```


## Recursos Adicionales

- Documentación Postman: https://learning.postman.com/
- Postman API: https://www.postman.com/postman/workspace/postman-public-workspace
- Newman: https://learning.postman.com/docs/running-collections/using-newman-cli/