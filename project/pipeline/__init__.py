from project.entity.config import (
    DataIngestionConfig,
    PrepareBasemodelConfig,
    PrepareCallbackConfig,
    TrainingConfig
)

from project.components.data_ingestion import DataIngestion 
from project.components.prepare_basemodel import PrepareBaseModel
from project.components.callbacks import CallBacks
from project.components.model_training import Training

from project.configeration import ConfigerationManager
from project.exception import CustomException
from project.logger import logging
import sys


class TrainingPipeline:
    """Pipeline orchestrator that runs data ingestion, base model preparation,
    callback preparation, and final model training sequentially."""

    def __init__(self):
        """Initialize configuration manager once."""
        self.config = ConfigerationManager()

    def run_data_ingestion(self):
        """Run the data ingestion pipeline."""
        try:
            logging.info(">>>>>>> Data Ingestion started <<<<<<<<<")
            data_ingestion_config = self.config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion.download_data()
            data_ingestion.extract_zip_file()
            logging.info(">>>>>>> Data Ingestion completed <<<<<<<<<")
        except Exception as e:
            raise CustomException(e, sys)

    def run_prepare_base_model(self):
        """Prepare the base model: load pretrained model and update layers."""
        try:
            logging.info(">>>>>>> Prepare Base Model started <<<<<<<<<")
            prepare_base_model_config = self.config.get_prepare_base_model_config()
            prepare_base_model = PrepareBaseModel(prepare_base_model_config)
            prepare_base_model.get_base_model()
            prepare_base_model.update_base_model()
            logging.info(">>>>>>> Prepare Base Model completed <<<<<<<<<")
        except Exception as e:
            raise CustomException(e, sys)

    def run_prepare_callbacks(self):
        """Prepare TensorBoard and ModelCheckpoint callbacks."""
        try:
            logging.info(">>>>>>> Prepare Callback started <<<<<<<<<")
            callback_config = self.config.get_prepare_callback_config()
            callback = CallBacks(callback_config)
            callback_list = callback.get_tb_ckpt_callbacks()
            logging.info(">>>>>>> Prepare Callback completed <<<<<<<<<")
            return callback_list
        except Exception as e:
            raise CustomException(e, sys)

    def run_model_training(self):
        """Train the model using configured generators and callbacks."""
        try:
            logging.info(">>>>>>> Model Training started <<<<<<<<<")

            model_training_config = self.config.get_training_config()
            model_training = Training(model_training_config)

            # MUST load base model before training
            model_training.get_base_model()

            model_training.train_valid_generator()

            # FIXED: correct callback method name
            callbacks = self.run_prepare_callbacks()

            model_training.train(callbacks=callbacks)

            logging.info(">>>>>>> Model Training completed <<<<<<<<<")
        except Exception as e:
            raise CustomException(e, sys)

    def run(self):
        """Execute the full machine learning pipeline."""
        try:
            logging.info(">>>>>>> Training Pipeline started <<<<<<<<<")
            self.run_data_ingestion()
            self.run_prepare_base_model()
            self.run_model_training()
            logging.info(">>>>>>> Training Pipeline completed <<<<<<<<<")
        except Exception as e:
            raise CustomException(e, sys)
