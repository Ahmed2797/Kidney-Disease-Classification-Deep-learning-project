from project.components.data_ingestion import DataIngestion 
from project.components.prepare_basemodel import PrepareBaseModel
from project.components.callbacks import CallBacks
from project.components.model_training import Training
from project.components.model_evalution import ModelEvaluation

from project.configeration import ConfigerationManager
from project.exception import CustomException
from project.logger import logging
import sys


class TrainingPipeline:
    """
    Orchestrates the complete machine learning workflow including:
    - Data ingestion
    - Base model preparation
    - Callback creation
    - Model training
    - Model evaluation
    
    This class executes each pipeline step sequentially using configurations
    provided by the ConfigerationManager.
    """

    def __init__(self):
        """
        Initialize the TrainingPipeline with a single instance of
        ConfigerationManager to access all configuration sections.
        """
        self.config = ConfigerationManager()

    def run_data_ingestion(self):
        """
        Execute the data ingestion pipeline.
        
        Steps:
        - Download the dataset from the specified URL.
        - Extract the downloaded zip file.
        
        Raises:
            CustomException: If any part of ingestion fails.
        """
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
        """
        Prepare the base model for training.
        
        Steps:
        - Load pretrained model architecture and weights.
        - Update top layers based on configuration.
        
        Raises:
            CustomException: If any part of base model preparation fails.
        """
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
        """
        Create required Keras callbacks such as:
        - TensorBoard callback
        - ModelCheckpoint callback
        
        Returns:
            list: List of prepared callbacks.
            
        Raises:
            CustomException: If callback preparation fails.
        """
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
        """
        Train the model using:
        - Loaded base model
        - Training & validation generators
        - Prepared callbacks
        
        Raises:
            CustomException: If model training fails.
        """
        try:
            logging.info(">>>>>>> Model Training started <<<<<<<<<")

            model_training_config = self.config.get_training_config()
            model_training = Training(model_training_config)

            # Load updated base model
            model_training.get_base_model()

            # Prepare train/validation generators
            model_training.train_valid_generator()

            # Prepare callbacks
            callbacks = self.run_prepare_callbacks()

            # Train the model
            model_training.train(callbacks=callbacks)

            logging.info(">>>>>>> Model Training completed <<<<<<<<<")
        except Exception as e:
            raise CustomException(e, sys)

    def run_model_evaluation(self):
        """
        Evaluate the trained model on the test dataset.
        
        Raises:
            CustomException: If evaluation fails.
        """
        try:
            logging.info(">>>>>>> Model Evaluation started <<<<<<<<<")
            model_evaluation_config = self.config.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(model_evaluation_config)
            model_evaluation.evaluate_model()
            logging.info(">>>>>>> Model Evaluation completed <<<<<<<<<")
        except Exception as e:
            raise CustomException(e, sys)

    def run(self):
        """
        Execute the full ML pipeline in order:
        1. Data ingestion
        2. Base model preparation
        3. Model training
        4. Model evaluation
        
        Raises:
            CustomException: If any stage of the pipeline fails.
        """
        try:
            logging.info(">>>>>>> Training Pipeline started <<<<<<<<<")
            self.run_data_ingestion()
            self.run_prepare_base_model()
            self.run_model_training()
            self.run_model_evaluation()
            logging.info(">>>>>>> Training Pipeline completed <<<<<<<<<")
        except Exception as e:
            raise CustomException(e, sys)
