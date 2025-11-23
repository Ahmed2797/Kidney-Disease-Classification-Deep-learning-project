from project.entity.config import PrepareBasemodelConfig
from project.components.prepare_basemodel import PrepareBaseModel
from project.configeration import ConfigerationManager
from project.exception import CustomException
from project.logger import logging
import sys

class PrepareBaseModelPipeline:
    def __init__(self):
        pass
    
    def main(self):
        try:
            config = ConfigerationManager()
            prepare_base_model_config = config.get_prepare_base_model_config()
            prepare_base_model = PrepareBaseModel(prepare_base_model_config)
            prepare_base_model.get_base_model()
            prepare_base_model.update_base_model()
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    try:
        pipeline = PrepareBaseModelPipeline()
        pipeline.main()
    except Exception as e:
        raise CustomException(e, sys)

    
    