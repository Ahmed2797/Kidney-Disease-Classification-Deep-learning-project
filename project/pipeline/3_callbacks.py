import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from project.components.callbacks import CallBacks
from project.configeration import ConfigerationManager
from project.exception import CustomException
from project.logger import logging






# Testing
class TestCallBacks:
    def __init__(self):
        pass
    def main(self):

        try:
            config = ConfigerationManager()
            callbacks_config = config.get_prepare_callback_config()
            callback = CallBacks(callbacks_config)
            callback_list = callback.get_tb_ckpt_callbacks()
            print(callback_list)
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        test = TestCallBacks()
        test.main()
    except Exception as e:
        raise CustomException(e, sys)