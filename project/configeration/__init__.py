from project.entity.config import DataIngestionConfig
from project.utils import read_yaml, create_directories
from project.exception import CustomException
import sys
from project.constants import CONFIG_YAML_FILE, PARAM_YAML_FILE


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
