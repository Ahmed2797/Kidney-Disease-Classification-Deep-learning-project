import os
import sys
import zipfile
import gdown
from project.logger import logging
from project.exception import CustomException
from project.entity.config import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        try:
            logging.info("Initializing Data Ingestion")
            self.config = config
        except Exception as e:
            raise CustomException(e, sys)

    def download_data(self):
        try:
            data_url = self.config.source_url
            zip_down_dir = self.config.local_data_file

            # create directory safely
            os.makedirs(self.config.root_dir, exist_ok=True)

            logging.info(f"Downloading data from {data_url} to {zip_down_dir}")

            # extract file id
            file_id = data_url.split('/')[-2]

            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            # download the file
            gdown.download(download_url, zip_down_dir)

            logging.info("Download completed successfully!")
        except Exception as e:
            raise CustomException(e, sys)

    def extract_zip_file(self):
        try:
            unzip_path = self.config.unzip_dir

            os.makedirs(unzip_path, exist_ok=True)

            with zipfile.ZipFile(self.config.local_data_file, 'r') as f:
                f.extractall(unzip_path)

            logging.info(f"Extraction completed at {unzip_path}")
        except Exception as e:
            raise CustomException(e, sys)
