from project.entity.config import DataIngestionConfig
from project.utils import read_yaml, create_directories
from project.exception import CustomException
import sys
from project.constants import CONFIG_YAML_FILE, PARAM_YAML_FILE



class ConfigerationManager:
    def __init__(self, config=CONFIG_YAML_FILE, param=PARAM_YAML_FILE):
        try:
            self.config = read_yaml(config)
            self.param = read_yaml(param)
            create_directories(self.config.artifacts_root)
        except Exception as e:
            raise CustomException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            config = self.config.data_ingestion
            
            create_directories(config.root_dir)

            return DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
            )
        except Exception as e:
            raise CustomException(e, sys)


        
