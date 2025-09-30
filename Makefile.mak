.PHONY: help install train test run docker-build docker-run docker-stop clean

help:
	@echo "Comandos disponibles:"
	@echo "  make install       - Instalar dependencias"
	@echo "  make train         - Entrenar el modelo"
	@echo "  make test          - Ejecutar tests"
	@echo "  make run           - Ejecutar API localmente"
	@echo "  make docker-build  - Construir imagen Docker"
	@echo "  make docker-run    - Ejecutar contenedor Docker"
	@echo "  make docker-stop   - Detener contenedor Docker"
	@echo "  make clean         - Limpiar archivos generados"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

train:
	python models/train_model.py

test:
	pytest tests/ -v --cov=api --cov-report=term-missing

run:
	python api/app.py

docker-build:
	docker build -t breast-cancer-api:latest .

docker-run:
	docker run -d --name breast-cancer-api -p 5000:5000 breast-cancer-api:latest

docker-stop:
	docker stop breast-cancer-api || true
	docker rm breast-cancer-api || true

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage