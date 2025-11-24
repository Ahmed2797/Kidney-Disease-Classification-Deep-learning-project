
from project.entity.config import (DataIngestionConfig,
PrepareBasemodelConfig,
PrepareCallbackConfig)

from project.components.data_ingestion import DataIngestion 
from project.components.prepare_basemodel import PrepareBaseModel
from project.components.callbacks import CallBacks



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
            config = ConfigerationManager()
            prepare_base_model_config = config.get_prepare_base_model_config()
            prepare_base_model = PrepareBaseModel(prepare_base_model_config)
            prepare_base_model.get_base_model()
            prepare_base_model.update_base_model()
            logging.info(">>>>>>> Prepare Base Model completed <<<<<<<<<")
        except Exception as e:
            raise CustomException(e, sys)
        
    def get_prepare_callback_pipeline(self):
        try:
            logging.info(">>>>>>> Prepare Callback started <<<<<<<<<")
            config = ConfigerationManager()
            callback_config = config.get_prepare_callback_config()
            callback = CallBacks(callback_config)
            callback_list=callback.get_tb_ckpt_callbacks()
            logging.info(">>>>>>> Prepare Callback completed <<<<<<<<<")
        except Exception as e:
            raise CustomException(e, sys)   

    

    def run(self):
        try:
            logging.info(">>>>>>> Training Pipeline started <<<<<<<<<")
            self.get_data_ingestion_pipeline()
            self.get_prepare_base_model_pipeline()
            self.get_prepare_callback_pipeline()
            logging.info(">>>>>>> Training Pipeline completed <<<<<<<<<")

        except Exception as e:
            raise CustomException(e, sys)
    
