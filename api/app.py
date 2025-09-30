"""
API REST para predicción de cáncer de mama.

Este módulo implementa una API Flask que expone el modelo de predicción
mediante endpoints REST con validación de datos y manejo de errores.
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Tuple

import joblib
import numpy as np
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

MODEL_PATH = os.path.join('models', 'breast_cancer_model.pkl')
SCALER_PATH = os.path.join('models', 'scaler.pkl')
METADATA_PATH = os.path.join('models', 'model_metadata.pkl')

REQUIRED_FEATURES = [
    'mean_radius', 'mean_texture', 'mean_perimeter', 'mean_area',
    'mean_smoothness', 'mean_compactness', 'mean_concavity',
    'mean_concave_points', 'mean_symmetry', 'mean_fractal_dimension',
    'radius_error', 'texture_error', 'perimeter_error', 'area_error',
    'smoothness_error', 'compactness_error', 'concavity_error',
    'concave_points_error', 'symmetry_error', 'fractal_dimension_error',
    'worst_radius', 'worst_texture', 'worst_perimeter', 'worst_area',
    'worst_smoothness', 'worst_compactness', 'worst_concavity',
    'worst_concave_points', 'worst_symmetry', 'worst_fractal_dimension'
]


class ModelPredictor:
    """
    Clase para cargar y ejecutar predicciones con el modelo.
    """

    def __init__(self):
        """
        Inicializa el predictor cargando el modelo y scaler.
        """
        self.model = None
        self.scaler = None
        self.metadata = None
        self.load_model()

    def load_model(self) -> None:
        """
        Carga el modelo, scaler y metadata desde disco.
        """
        try:
            logger.info("Cargando modelo desde disco")
            self.model = joblib.load(MODEL_PATH)
            self.scaler = joblib.load(SCALER_PATH)
            self.metadata = joblib.load(METADATA_PATH)
            logger.info("Modelo cargado exitosamente")
            logger.info(f"Fecha de entrenamiento: {self.metadata.get('training_date', 'N/A')}")
        except FileNotFoundError as e:
            logger.error(f"Error al cargar modelo: {e}")
            raise RuntimeError("Modelo no encontrado. Ejecute train_model.py primero.")
        except Exception as e:
            logger.error(f"Error inesperado al cargar modelo: {e}")
            raise

    def validate_input(self, data: Dict) -> Tuple[bool, List[str]]:
        """
        Valida que el input contenga todas las features requeridas.

        Args:
            data: Diccionario con los datos de entrada

        Returns:
            Tupla (es_valido, lista_de_errores)
        """
        missing_features = [f for f in REQUIRED_FEATURES if f not in data]
        
        if missing_features:
            return False, missing_features
        
        try:
            for feature in REQUIRED_FEATURES:
                float(data[feature])
        except (ValueError, TypeError):
            return False, [f"Feature '{feature}' debe ser un número"]
        
        return True, []

    def predict(self, data: Dict) -> Dict:
        """
        Realiza una predicción basada en los datos de entrada.

        Args:
            data: Diccionario con las features

        Returns:
            Diccionario con la predicción y probabilidades
        """
        try:
            features = np.array([[data[f] for f in REQUIRED_FEATURES]])
            
            features_scaled = self.scaler.transform(features)
            
            prediction = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]
            
            target_names = self.metadata.get('target_names', ['malignant', 'benign'])
            prediction_label = target_names[prediction]
            
            result = {
                'prediction': int(prediction),
                'prediction_label': prediction_label.capitalize(),
                'probability': {
                    target_names[0].capitalize(): float(probabilities[0]),
                    target_names[1].capitalize(): float(probabilities[1])
                },
                'confidence': float(max(probabilities)),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Predicción realizada: {prediction_label} (confianza: {max(probabilities):.2f})")
            
            return result
        
        except Exception as e:
            logger.error(f"Error en predicción: {e}")
            raise


predictor = ModelPredictor()


@app.route('/', methods=['GET'])
def health_check():
    """
    Endpoint de verificación del estado del servicio.

    Returns:
        JSON con el estado del servicio
    """
    try:
        response = {
            'status': 'ok',
            'message': 'Breast Cancer Prediction API is running',
            'version': '1.0.0',
            'model_info': {
                'type': predictor.metadata.get('model_type', 'N/A'),
                'training_date': predictor.metadata.get('training_date', 'N/A'),
                'features_count': len(REQUIRED_FEATURES)
            },
            'timestamp': datetime.now().isoformat()
        }
        logger.info("Health check solicitado")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint para realizar predicciones.

    Espera un JSON con todas las features requeridas.

    Returns:
        JSON con la predicción y probabilidades
    """
    try:
        if not request.is_json:
            logger.warning("Request sin Content-Type: application/json")
            return jsonify({
                'error': 'Invalid content type',
                'message': 'Content-Type debe ser application/json'
            }), 400
        
        data = request.get_json()
        
        if not data:
            logger.warning("Request body vacío")
            return jsonify({
                'error': 'Empty request',
                'message': 'El body no puede estar vacío'
            }), 400
        
        is_valid, errors = predictor.validate_input(data)
        
        if not is_valid:
            logger.warning(f"Validación fallida: {errors}")
            return jsonify({
                'error': 'Invalid input',
                'message': 'Faltan features requeridas o valores inválidos',
                'missing_features': errors,
                'required_features': REQUIRED_FEATURES
            }), 400
        
        result = predictor.predict(data)
        
        return jsonify(result), 200
    
    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return jsonify({
            'error': 'Bad request',
            'message': str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Error inesperado en predicción: {e}")
        return jsonify({
            'error': 'Prediction failed',
            'message': 'Error interno del servidor'
        }), 500


@app.route('/features', methods=['GET'])
def get_features():
    """
    Endpoint para obtener la lista de features requeridas.

    Returns:
        JSON con las features requeridas
    """
    try:
        response = {
            'features': REQUIRED_FEATURES,
            'count': len(REQUIRED_FEATURES),
            'description': 'Lista de features requeridas para predicción'
        }
        logger.info("Lista de features solicitada")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error obteniendo features: {e}")
        return jsonify({
            'error': 'Error',
            'message': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """
    Manejador de errores 404.
    """
    return jsonify({
        'error': 'Not found',
        'message': 'Endpoint no encontrado'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Manejador de errores 500.
    """
    logger.error(f"Error 500: {error}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Error interno del servidor'
    }), 500


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("Iniciando API de predicción de cáncer de mama")
    logger.info("=" * 60)
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)