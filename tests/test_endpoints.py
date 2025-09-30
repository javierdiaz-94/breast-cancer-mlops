"""
Tests unitarios y de integración para la API.

Este módulo contiene tests para verificar el correcto funcionamiento
de todos los endpoints de la API.
"""

import json
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.app import app


@pytest.fixture
def client():
    """
    Fixture para crear un cliente de prueba de Flask.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """
    Test del endpoint de health check.
    """
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'ok'
    assert 'message' in data
    assert 'version' in data
    assert 'model_info' in data


def test_predict_valid_malignant(client):
    """
    Test de predicción con datos válidos de caso maligno.
    """
    payload = {
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
    
    response = client.post(
        '/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'prediction' in data
    assert 'prediction_label' in data
    assert 'probability' in data
    assert 'confidence' in data
    assert 'timestamp' in data


def test_predict_valid_benign(client):
    """
    Test de predicción con datos válidos de caso benigno.
    """
    payload = {
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
    
    response = client.post(
        '/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'prediction' in data
    assert 'prediction_label' in data


def test_predict_missing_features(client):
    """
    Test de predicción con features faltantes.
    """
    payload = {
        "mean_radius": 20.57,
        "mean_texture": 17.77
    }
    
    response = client.post(
        '/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Invalid input'


def test_predict_empty_body(client):
    """
    Test de predicción con body vacío.
    """
    response = client.post(
        '/predict',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_predict_invalid_content_type(client):
    """
    Test de predicción con Content-Type inválido.
    """
    response = client.post(
        '/predict',
        data='invalid data',
        content_type='text/plain'
    )
    
    assert response.status_code == 400


def test_predict_invalid_values(client):
    """
    Test de predicción con valores no numéricos.
    """
    payload = {
        "mean_radius": "not_a_number",
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
    
    response = client.post(
        '/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_get_features(client):
    """
    Test del endpoint de features.
    """
    response = client.get('/features')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'features' in data
    assert 'count' in data
    assert data['count'] == 30


def test_not_found(client):
    """
    Test de endpoint no existente.
    """
    response = client.get('/nonexistent')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])