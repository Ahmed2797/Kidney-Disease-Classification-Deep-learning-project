
from project.entity.config import DataIngestionConfig
from project.components.data_ingestion import DataIngestion
from project.configeration import ConfigerationManager
from project.exception import CustomException
from project.logger import logging
import sys



class Traning_Pipeline:
    def __init__(self):
        pass
    
    def get_data_ingestion_pipeline(self):
        try:
            logging.info(">>>>>>> Data Ingestion started <<<<<<<<<")
            config = ConfigerationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion.download_data()
            data_ingestion.extract_zip_file()
            logging.info(">>>>>>> Data Ingestion completed <<<<<<<<<")
        except Exception as e:
            raise CustomException(e, sys) 

    def get_prepare_base_model_pipeline(self):
        try:
            logging.info(">>>>>>> Prepare Base Model started <<<<<<<<<")
            pass
            logging.info(">>>>>>> Prepare Base Model completed <<<<<<<<<")
        except Exception as e:
            raise CustomException(e, sys)

    

    def run(self):
        try:
            logging.info(">>>>>>> Training Pipeline started <<<<<<<<<")
            self.get_data_ingestion_pipeline()
            self.get_prepare_base_model_pipeline()
            logging.info(">>>>>>> Training Pipeline completed <<<<<<<<<")

        except Exception as e:
            raise CustomException(e, sys)
    
