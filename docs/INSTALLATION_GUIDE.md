# Guía de Instalación y Despliegue

## Sistema MLOps: Predicción de Cáncer de Mama

### Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación Local](#instalación-local)
3. [Despliegue con Docker](#despliegue-con-docker)
4. [Configuración de CI/CD](#configuración-de-cicd)
5. [Verificación de Instalación](#verificación-de-instalación)
6. [Troubleshooting](#troubleshooting)

---

## Requisitos del Sistema

### Software Requerido

- **Python:** Versión 3.9 o superior
- **pip:** Gestor de paquetes de Python
- **Docker:** Versión 20.10 o superior
- **Git:** Para control de versiones
- **Postman:** Para pruebas de API (opcional pero recomendado)

### Especificaciones de Hardware Mínimas

- **CPU:** 2 cores
- **RAM:** 4 GB
- **Disco:** 2 GB de espacio libre
- **Sistema Operativo:** Windows 10+, macOS 10.14+, o Linux (Ubuntu 20.04+)

### Verificar Instalaciones

```bash
# Verificar Python
python --version
# Salida esperada: Python 3.9.x o superior

# Verificar pip
pip --version

# Verificar Docker
docker --version
# Salida esperada: Docker version 20.10.x o superior

# Verificar Git
git --version
```

---

## Instalación Local

### Paso 1: Clonar el Repositorio

```bash
# Clonar desde GitHub
git clone https://github.com/tu-usuario/breast-cancer-mlops.git

# Navegar al directorio
cd breast-cancer-mlops
```

### Paso 2: Crear Entorno Virtual

#### En Windows:

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate
```

#### En macOS/Linux:

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

Cuando el entorno esté activado, verás `(venv)` en tu prompt.

### Paso 3: Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

Este proceso puede tomar varios minutos dependiendo de tu conexión a internet.

### Paso 4: Entrenar el Modelo

```bash
# Ejecutar script de entrenamiento
python models/train_model.py
```

**Salida esperada:**

```
============================================================
Iniciando entrenamiento del modelo
============================================================
2025-09-29 10:00:00 - INFO - Cargando dataset Breast Cancer Wisconsin
2025-09-29 10:00:01 - INFO - Dataset cargado: 569 muestras, 30 features
2025-09-29 10:00:01 - INFO - Clases: ['malignant' 'benign']
2025-09-29 10:00:01 - INFO - Dividiendo datos en train/test
2025-09-29 10:00:01 - INFO - Train size: 455, Test size: 114
2025-09-29 10:00:01 - INFO - Normalizando features con StandardScaler
2025-09-29 10:00:01 - INFO - Entrenando modelo Random Forest
2025-09-29 10:00:03 - INFO - Modelo entrenado exitosamente
2025-09-29 10:00:03 - INFO - Evaluando modelo
2025-09-29 10:00:03 - INFO - Train Accuracy: 1.0000
2025-09-29 10:00:03 - INFO - Test Accuracy: 0.9649
2025-09-29 10:00:03 - INFO - Test Precision: 0.9655
2025-09-29 10:00:03 - INFO - Test Recall: 0.9649
2025-09-29 10:00:03 - INFO - Test F1-Score: 0.9649
...
2025-09-29 10:00:05 - INFO - Modelo guardado en: models/breast_cancer_model.pkl
============================================================
Entrenamiento completado exitosamente
============================================================
```

### Paso 5: Verificar Archivos Generados

```bash
# Listar archivos del modelo
ls -la models/
```

Deberías ver:

- `breast_cancer_model.pkl`
- `scaler.pkl`
- `model_metadata.pkl`

### Paso 6: Ejecutar la API

```bash
# Iniciar servidor Flask
python api/app.py
```

**Salida esperada:**

```
============================================================
Iniciando API de predicción de cáncer de mama
============================================================
2025-09-29 10:10:00 - INFO - Cargando modelo desde disco
2025-09-29 10:10:01 - INFO - Modelo cargado exitosamente
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

La API ahora está disponible en `http://localhost:5000`

### Paso 7: Probar la API

En otra terminal (manteniendo la API corriendo):

```bash
# Activar entorno virtual si es necesario
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate  # Windows

# Ejecutar tests
pytest tests/ -v
```

---

## Despliegue con Docker

### Paso 1: Preparar el Proyecto

Asegúrate de tener el modelo entrenado:

```bash
python models/train_model.py
```

### Paso 2: Construir la Imagen Docker

```bash
# Construir imagen
docker build -t breast-cancer-api:latest .
```

Este proceso puede tomar 5-10 minutos la primera vez.

**Salida esperada:**

```
[+] Building 120.5s (15/15) FINISHED
 => [internal] load build definition
 => => transferring dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.9-slim
 ...
 => exporting to image
 => => exporting layers
 => => writing image sha256:abc123...
 => => naming to docker.io/library/breast-cancer-api:latest
```

### Paso 3: Verificar la Imagen

```bash
# Listar imágenes Docker
docker images | grep breast-cancer-api
```

Deberías ver:

```
breast-cancer-api    latest    abc123def456    2 minutes ago    500MB
```

### Paso 4: Ejecutar el Contenedor

```bash
# Ejecutar contenedor
docker run -d \
  --name breast-cancer-api \
  -p 5000:5000 \
  breast-cancer-api:latest
```

Parámetros:

- `-d`: Ejecutar en background (detached)
- `--name`: Nombre del contenedor
- `-p 5000:5000`: Mapear puerto 5000 del host al puerto 5000 del contenedor

### Paso 5: Verificar Contenedor Corriendo

```bash
# Ver contenedores activos
docker ps
```

Salida esperada:

```
CONTAINER ID   IMAGE                        COMMAND              STATUS         PORTS
abc123def456   breast-cancer-api:latest     "python api/app.py"  Up 2 minutes   0.0.0.0:5000->5000/tcp
```

### Paso 6: Ver Logs del Contenedor

```bash
# Ver logs en tiempo real
docker logs -f breast-cancer-api
```

Para detener el seguimiento de logs: `Ctrl+C`

### Comandos Útiles de Docker

```bash
# Detener contenedor
docker stop breast-cancer-api

# Iniciar contenedor detenido
docker start breast-cancer-api

# Reiniciar contenedor
docker restart breast-cancer-api

# Eliminar contenedor
docker rm breast-cancer-api

# Eliminar imagen
docker rmi breast-cancer-api:latest

# Ver logs (últimas 100 líneas)
docker logs --tail 100 breast-cancer-api

# Ejecutar comando dentro del contenedor
docker exec -it breast-cancer-api /bin/bash

# Ver uso de recursos
docker stats breast-cancer-api
```

---

## Configuración de CI/CD

### Configuración de GitHub Actions

#### Paso 1: Preparar Repositorio GitHub

```bash
# Inicializar repositorio Git (si no existe)
git init

# Agregar archivos
git add .

# Commit inicial
git commit -m "Initial commit: MLOps breast cancer prediction"

# Agregar remote
git remote add origin https://github.com/tu-usuario/breast-cancer-mlops.git

# Push a GitHub
git push -u origin main
```

#### Paso 2: Configurar Secrets (Opcional)

Para publicar en Docker Hub:

1. Ir a tu repositorio en GitHub
2. Click en "Settings"
3. Click en "Secrets and variables" > "Actions"
4. Click en "New repository secret"
5. Agregar:
   - Name: `DOCKER_USERNAME`
   - Value: Tu username de Docker Hub
6. Agregar otro secret:
   - Name: `DOCKER_PASSWORD`
   - Value: Tu password o access token de Docker Hub

#### Paso 3: Verificar Workflow

El workflow se ejecutará automáticamente con cada push a main o develop.

Para ver el estado:

1. Ir a tu repositorio en GitHub
2. Click en la pestaña "Actions"
3. Ver el estado de los workflows

---

## Verificación de Instalación

### 1. Verificar Health Check

#### Con navegador:

Abrir: `http://localhost:5000/`

#### Con línea de comandos:

```bash
# Windows (PowerShell)
Invoke-WebRequest -Uri http://localhost:5000/ | Select-Object -Expand Content

# macOS/Linux
curl http://localhost:5000/
```

**Respuesta esperada:**

```json
{
    "status": "ok",
    "message": "Breast Cancer Prediction API is running",
    "version": "1.0.0"
}
```

### 2. Prueba de Predicción con Postman

Ver guía completa en `POSTMAN_GUIDE.md`

### 3. Ejecutar Suite de Tests

```bash
# Activar entorno virtual
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate  # Windows

# Ejecutar todos los tests
pytest tests/ -v

# Con reporte de cobertura
pytest tests/ --cov=api --cov-report=html

# Ver reporte HTML
# macOS
open htmlcov/index.html
# Linux
xdg-open htmlcov/index.html
# Windows
start htmlcov/index.html
```

---

## Troubleshooting

### Problema: Python no reconocido

**Error:**

```
'python' is not recognized as an internal or external command
```

**Solución:**

- Instalar Python desde https://www.python.org/downloads/
- Durante instalación, marcar "Add Python to PATH"
- Reiniciar terminal

### Problema: Puerto 5000 en uso

**Error:**

```
OSError: [Errno 48] Address already in use
```

**Solución:**

```bash
# Ver qué está usando el puerto 5000
# macOS/Linux
lsof -i :5000

# Windows
netstat -ano | findstr :5000

# Matar proceso
# macOS/Linux
kill -9 <PID>

# Windows
taskkill /PID <PID> /F

# O usar otro puerto
PORT=5001 python api/app.py
```

### Problema: Modelo no encontrado

**Error:**

```
FileNotFoundError: [Errno 2] No such file or directory: 'models/breast_cancer_model.pkl'
```

**Solución:**

```bash
# Entrenar el modelo
python models/train_model.py

# Verificar que se crearon los archivos
ls models/
```

### Problema: Docker no inicia

**Error:**

```
Cannot connect to the Docker daemon
```

**Solución:**

- Iniciar Docker Desktop (Windows/macOS)
- En Linux:
  ```bash
  sudo systemctl start docker
  ```

### Problema: Error al construir imagen Docker

**Error:**

```
failed to solve with frontend dockerfile.v0
```

**Solución:**

```bash
# Limpiar caché de Docker
docker system prune -a

# Reconstruir
docker build --no-cache -t breast-cancer-api:latest .
```

### Problema: Tests fallan

**Error:**

```
ModuleNotFoundError: No module named 'flask'
```

**Solución:**

```bash
# Asegurarse de estar en el entorno virtual
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: Permisos en Docker

**Error:**

```
Permission denied
```

**Solución (Linux):**

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Cerrar sesión y volver a iniciar
```

---

## Contacto y Soporte

Para problemas o preguntas:

1. Revisar la documentación en `README.md`
2. Consultar issues existentes en GitHub
3. Crear un nuevo issue con:
   - Descripción del problema
   - Pasos para reproducir
   - Logs relevantes
   - Sistema operativo y versiones

---

## Próximos Pasos

Una vez completada la instalación:

1. Revisar `README.md` para información general
2. Consultar `POSTMAN_GUIDE.md` para pruebas de API
3. Explorar el código en `models/train_model.py` y `api/app.py`
4. Experimentar con diferentes configuraciones del modelo
5. Implementar mejoras y nuevas features