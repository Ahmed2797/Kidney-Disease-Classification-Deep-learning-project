from project.entity.config import (DataIngestionConfig,
                                  PrepareBasemodelConfig)
from project.utils import read_yaml, create_directories
from project.exception import CustomException
import sys
from project.constants import *


class ConfigerationManager:
    """
    Manages the loading and parsing of configuration and parameter YAML files.
    Creates required directories and provides configuration objects 
    for different pipeline components.
    """

    def __init__(self, config=CONFIG_YAML_FILE, param=PARAM_YAML_FILE):
        """
        Initialize the Configuration Manager.

        Args:
            config (str): Path to the main configuration YAML file.
            param (str): Path to the parameters YAML file.

        Raises:
            CustomException: If YAML reading or directory creation fails.
        """
        try:
            self.config = read_yaml(config)
            self.param = read_yaml(param)
            create_directories(self.config.artifacts_root)
        except Exception as e:
            raise CustomException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Creates and returns the DataIngestionConfig object 
        by reading values from the config YAML file.

        Returns:
            DataIngestionConfig: Configuration object for data ingestion.

        Steps:
            - Extract data ingestion section from config YAML
            - Ensure root directory exists
            - Populate DataIngestionConfig dataclass with YAML values

        Raises:
            CustomException: If extraction or object creation fails.
        """
        try:
            config = self.config.data_ingestion

            # Create root directory for data ingestion
            create_directories(config.root_dir)

            return DataIngestionConfig(
                root_dir=config.root_dir,
                source_url=config.source_url,
                local_data_file=config.local_data_file,
                unzip_dir=config.unzip_dir,
            )
        except Exception as e:
            raise CustomException(e, sys)



    def get_prepare_base_model_config(self)-> PrepareBasemodelConfig:
        """
        Creates and returns the PrepareBasemodelConfig object 
        by reading values from the config YAML file.

        Returns:
            PrepareBasemodelConfig: Configuration object for base model preparation.

        Steps:
            - Extract prepare base model section from config YAML
            - Ensure root directory exists
            - Populate PrepareBasemodelConfig dataclass with YAML values

        Raises:
            CustomException: If extraction or object creation fails.
        """
        try:
            config = self.config.prepare_base_model

            # Create root directory for base model preparation
            create_directories(config.root_dir)

            prepare_base_model_config = PrepareBasemodelConfig(
            root_dir=config.root_dir,
            base_model=config.base_model,
            update_base_model=config.update_base_model,
            param_image_size=self.param.IMAGE_SIZE, 
            param_batch_size=self.param.BATCH_SIZE,
            param_epochs=self.param.EPOCHS, 
            param_learning_rate=self.param.LEARNING_RATE, 
            param_classics=self.param.CLASSICS, 
            param_weight=self.param.WEIGHTS, 
            param_include_top=self.param.INCLUDETOP
            )
        
            return prepare_base_model_config
        except Exception as e:
            raise CustomException(e, sys)