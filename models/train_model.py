"""
Módulo para entrenar y serializar el modelo de predicción de cáncer de mama.

Este módulo carga el dataset Breast Cancer Wisconsin, entrena un modelo
Random Forest y lo guarda para su uso posterior en la API.
"""

import os
import logging
from datetime import datetime
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BreastCancerModelTrainer:
    """
    Clase para entrenar y evaluar el modelo de predicción de cáncer de mama.
    """

    def __init__(self, test_size: float = 0.2, random_state: int = 42):
        """
        Inicializa el entrenador del modelo.

        Args:
            test_size: Proporción del dataset para testing
            random_state: Semilla para reproducibilidad
        """
        self.test_size = test_size
        self.random_state = random_state
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.target_names = None

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Carga el dataset Breast Cancer Wisconsin.

        Returns:
            Tupla con features (X) y target (y)
        """
        logger.info("Cargando dataset Breast Cancer Wisconsin")
        
        data = load_breast_cancer()
        X = pd.DataFrame(data.data, columns=data.feature_names)
        y = pd.Series(data.target, name='target')
        
        self.feature_names = data.feature_names
        self.target_names = data.target_names
        
        logger.info(f"Dataset cargado: {X.shape[0]} muestras, {X.shape[1]} features")
        logger.info(f"Clases: {self.target_names}")
        
        return X, y

    def preprocess_data(
        self,
        X: pd.DataFrame,
        y: pd.Series
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Preprocesa los datos: división train/test y normalización.

        Args:
            X: Features
            y: Target

        Returns:
            Tupla con X_train, X_test, y_train, y_test
        """
        logger.info("Dividiendo datos en train/test")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=y
        )
        
        logger.info(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")
        
        logger.info("Normalizando features con StandardScaler")
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train.values, y_test.values

    def train_model(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Entrena el modelo Random Forest.

        Args:
            X_train: Features de entrenamiento
            y_train: Target de entrenamiento
        """
        logger.info("Entrenando modelo Random Forest")
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=self.random_state,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        logger.info("Modelo entrenado exitosamente")

    def evaluate_model(
        self,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_train: np.ndarray,
        y_test: np.ndarray
    ) -> dict:
        """
        Evalúa el rendimiento del modelo.

        Args:
            X_train: Features de entrenamiento
            X_test: Features de testing
            y_train: Target de entrenamiento
            y_test: Target de testing

        Returns:
            Diccionario con métricas de evaluación
        """
        logger.info("Evaluando modelo")
        
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        train_accuracy = accuracy_score(y_train, y_train_pred)
        test_accuracy = accuracy_score(y_test, y_test_pred)
        test_precision = precision_score(y_test, y_test_pred, average='weighted')
        test_recall = recall_score(y_test, y_test_pred, average='weighted')
        test_f1 = f1_score(y_test, y_test_pred, average='weighted')
        
        logger.info(f"Train Accuracy: {train_accuracy:.4f}")
        logger.info(f"Test Accuracy: {test_accuracy:.4f}")
        logger.info(f"Test Precision: {test_precision:.4f}")
        logger.info(f"Test Recall: {test_recall:.4f}")
        logger.info(f"Test F1-Score: {test_f1:.4f}")
        
        logger.info("\nReporte de Clasificación:")
        print(classification_report(y_test, y_test_pred, target_names=self.target_names))
        
        logger.info("\nMatriz de Confusión:")
        print(confusion_matrix(y_test, y_test_pred))
        
        cv_scores = cross_val_score(
            self.model, X_train, y_train,
            cv=5, scoring='accuracy'
        )
        logger.info(f"\nCross-validation scores: {cv_scores}")
        logger.info(f"CV Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        logger.info("\nTop 10 Features más importantes:")
        print(feature_importance.head(10))
        
        metrics = {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'test_precision': test_precision,
            'test_recall': test_recall,
            'test_f1': test_f1,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'training_date': datetime.now().isoformat(),
            'n_samples_train': len(X_train),
            'n_samples_test': len(X_test),
            'n_features': len(self.feature_names)
        }
        
        return metrics

    def save_model(self, model_dir: str = 'models') -> None:
        """
        Guarda el modelo y el scaler en disco.

        Args:
            model_dir: Directorio donde guardar los archivos
        """
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            logger.info(f"Directorio {model_dir} creado")
        
        model_path = os.path.join(model_dir, 'breast_cancer_model.pkl')
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        metadata_path = os.path.join(model_dir, 'model_metadata.pkl')
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        
        metadata = {
            'feature_names': self.feature_names,
            'target_names': self.target_names,
            'model_type': 'RandomForestClassifier',
            'training_date': datetime.now().isoformat()
        }
        joblib.dump(metadata, metadata_path)
        
        logger.info(f"Modelo guardado en: {model_path}")
        logger.info(f"Scaler guardado en: {scaler_path}")
        logger.info(f"Metadata guardada en: {metadata_path}")


def main():
    """
    Función principal para entrenar y guardar el modelo.
    """
    logger.info("=" * 60)
    logger.info("Iniciando entrenamiento del modelo")
    logger.info("=" * 60)
    
    trainer = BreastCancerModelTrainer(test_size=0.2, random_state=42)
    
    X, y = trainer.load_data()
    
    X_train, X_test, y_train, y_test = trainer.preprocess_data(X, y)
    
    trainer.train_model(X_train, y_train)
    
    metrics = trainer.evaluate_model(X_train, X_test, y_train, y_test)
    
    trainer.save_model()
    
    logger.info("=" * 60)
    logger.info("Entrenamiento completado exitosamente")
    logger.info("=" * 60)
    
    return metrics


if __name__ == '__main__':
    main()