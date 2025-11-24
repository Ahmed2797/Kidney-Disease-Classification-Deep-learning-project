from project.entity.config import PrepareCallbackConfig 
from project.components.callbacks import CallBacks
from project.configeration import ConfigerationManager
from project.exception import CustomException
from project.logger import logging
import tensorflow as tf
import sys
import os
import time





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
        self.config = config

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
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        tb_log_dir = os.path.join(
            self.config.tensorboard_root_log_dir,
            f"tb_logs_at_{timestamp}"
        )
        return tf.keras.callbacks.TensorBoard(log_dir=tb_log_dir)

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
        return tf.keras.callbacks.ModelCheckpoint(
            filepath=self.config.checkpoint_model_filepath,
            save_best_only=True
        )

    def get_tb_ckpt_callbacks(self) -> list:
        """
        Returns a list of callbacks required during training.

        Returns:
            list: Contains TensorBoard and ModelCheckpoint callbacks.
        """
        return [self.create_tb_callback, self.create_ckpt_callback]


# Testing

if __name__ == '__main__':
    try:
        config = ConfigerationManager()
        callbacks_config = config.get_prepare_callback_config()
        callback = CallBacks(callbacks_config)
        callback_list = callback.get_tb_ckpt_callbacks()
        print(callback_list)
    except Exception as e:
        raise 
