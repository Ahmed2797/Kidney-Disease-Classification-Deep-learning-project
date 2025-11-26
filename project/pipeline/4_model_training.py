import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from project.configeration import ConfigerationManager 
from project.components.callbacks import CallBacks
from project.exception import CustomException
from project.logger import logging
from project.components.model_training import Training



class TraningPipeline:
    def __init__(self):
        pass
    def main(self):
        

        try:
            # Initialize configuration manager
            config = ConfigerationManager()  

            # Prepare callbacks (optional, uncomment if needed)
            callbacks_config = config.get_prepare_callback_config()
            callback_list = CallBacks(config=callbacks_config).get_tb_ckpt_callbacks()

            # Training setup
            training_config = config.get_training_config()
            trainer = Training(config=training_config)  # fixed spelling from 'Traning'

            # Prepare model and data
            trainer.get_base_model()
            trainer.train_valid_generator()
            trainer.train()

            # Train the model (uncomment when callbacks are ready)
            trainer.train(callbacks=callback_list)

        except Exception as e:
            raise CustomException (e,sys)

if __name__ == "__main__":
    try:
        pipeline = TraningPipeline()
        pipeline.main()
    except Exception as e:
        raise CustomException(e, sys)