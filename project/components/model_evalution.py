import sys
import os
import yaml

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pathlib import Path
import tensorflow as tf
import mlflow
from project.entity.config import ModelEvaluationConfig
from project.utils import save_json


class Evaluation:
    """
    Handles model evaluation, saving scores, and logging metrics/models to MLflow.
    """

    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    # ---------------------------------------------------------------------
    def _valid_generator(self):
        """Create validation dataset."""
        img_size = tuple(self.config.param_image_size[:-1])
        batch_size = self.config.param_batch_size

        val_ds = tf.keras.utils.image_dataset_from_directory(
            self.config.training_data_path,
            validation_split=0.30,
            subset="validation",
            seed=42,
            image_size=img_size,
            batch_size=batch_size,
            shuffle=False,
            label_mode='categorical',
        )

        normalization_layer = tf.keras.layers.Rescaling(1.0 / 255)
        val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
        self.valid_generator = val_ds.prefetch(buffer_size=tf.data.AUTOTUNE)

    # ---------------------------------------------------------------------
    @staticmethod
    def load_model(model_path: Path):
        """Load the trained model."""
        return tf.keras.models.load_model(model_path)

    # ---------------------------------------------------------------------
    def evalution(self):
        """Evaluate the model and return loss, accuracy as a dictionary."""
        self._valid_generator()
        model = self.load_model(Path("artifacts/training/model.h5"))
        loss, accuracy = model.evaluate(self.valid_generator)

        return {
            "loss": float(loss),
            "accuracy": float(accuracy)
        }

    # ---------------------------------------------------------------------
    def save_outputs(self):
        """
        Runs evaluation ONCE and saves:
            - report.json
            - scores.json
            - report.yaml
        """
        results = self.evalution()

        # 1. Save report.json  
        report_path = Path(self.config.report_file_dir) / self.config.report_file
        report_path.parent.mkdir(parents=True, exist_ok=True)
        save_json(path=report_path, data=results)

        # 2. Save scores.json
        scores_path = Path(self.config.scores_file_dir) / self.config.scores_file
        scores_path.parent.mkdir(parents=True, exist_ok=True)
        save_json(path=scores_path, data=results)

        # 3. Save report.yaml
        yaml_path = Path("artifacts/model_evaluation/report.yaml")
        yaml_path.parent.mkdir(parents=True, exist_ok=True)

        with open(yaml_path, "w") as f:
            yaml.safe_dump(results, f)

        return results

    # ---------------------------------------------------------------------
    def log_mlflow(self):
        """Log metrics and model to MLflow."""
        os.environ["MLFLOW_TRACKING_USERNAME"] = "Ahmed2797"
        os.environ["MLFLOW_TRACKING_PASSWORD"] = "466cd6e40b4463c19cee521d93d34f35fb915367"

        mlflow.set_tracking_uri(self.config.mlflow_tracking_uri)
        mlflow.set_experiment(self.config.mlflow_experiment_name)

        results = self.evalution()

        with mlflow.start_run():
            mlflow.log_params(self.config.all_params)
            mlflow.log_metric("val_loss", results["loss"])
            mlflow.log_metric("val_accuracy", results["accuracy"])

            model = self.load_model(Path("artifacts/training/model.h5"))

            export_dir = Path("artifacts/training/model_export")
            export_dir.mkdir(parents=True, exist_ok=True)
            model.export(export_dir)

            mlflow.log_artifacts(str(export_dir), artifact_path="model")
