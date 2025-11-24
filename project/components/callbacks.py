import os
import time
import tensorflow as tf
from project.entity.config import PrepareCallbackConfig
from project.exception import CustomException
from project.logger import logging
import sys


class CallBacks:
    """
    Creates TensorBoard and ModelCheckpoint callbacks for training.

    Args:
        config (PrepareCallbackConfig): Dataclass containing callback paths.

    Methods:
        create_tb_callback (property): Returns TensorBoard callback.
        create_ckpt_callback (property): Returns ModelCheckpoint callback.
        get_tb_ckpt_callbacks: Returns list of both callbacks.
    """

    def __init__(self, config: PrepareCallbackConfig):
        """Store callback configuration."""
        try:
            self.config = config
        except Exception as e:
            raise CustomException(e, sys)

    @property
    def create_tb_callback(self) -> tf.keras.callbacks.TensorBoard:
        """
        Create and return a TensorBoard callback.

        Behavior:
            - Creates a unique timestamped log directory inside the root log dir.
            - Helps visualize training metrics like loss, accuracy, graphs.

        Returns:
            TensorBoard: Keras TensorBoard callback instance.
        """
        try:
            timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
            tb_log_dir = os.path.join(
                self.config.tensorboard_root_log_dir,
                f"tb_logs_at_{timestamp}"
            )
            return tf.keras.callbacks.TensorBoard(log_dir=tb_log_dir)
        except Exception as e:
            raise CustomException(e, sys)

    @property
    def create_ckpt_callback(self) -> tf.keras.callbacks.ModelCheckpoint:
        """
        Create and return a ModelCheckpoint callback.

        Behavior:
            - Saves only the best model based on validation performance.
            - Stores model file at the configured checkpoint path.

        Returns:
            ModelCheckpoint: Keras model checkpoint callback instance.
        """
        try:    
            return tf.keras.callbacks.ModelCheckpoint(
                filepath=self.config.checkpoint_model_filepath,
                save_best_only=True
            )
        except Exception as e:
            raise CustomException(e, sys)

    def get_tb_ckpt_callbacks(self) -> list:
        """
        Returns a list of callbacks required during training.

        Returns:
            list: Contains TensorBoard and ModelCheckpoint callbacks.
        """
        try:    
            return [self.create_tb_callback, self.create_ckpt_callback]
        except Exception as e:
            raise CustomException(e, sys)

