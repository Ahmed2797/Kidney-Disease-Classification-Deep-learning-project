import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from project.components.data_ingestion import DataIngestion
from project.configeration import ConfigerationManager
from project.exception import CustomException
from project.logger import logging
import sys

class DataIngestionPipeline:
    def __init__(self):
        pass
    
    def main(self):
        try:
            config = ConfigerationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion.download_data()
            data_ingestion.extract_zip_file()
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    try:
        pipeline = DataIngestionPipeline()
        pipeline.main()
    except Exception as e:
        raise CustomException(e, sys)

    
    