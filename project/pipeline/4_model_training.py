import math
import tensorflow as tf
from pathlib import Path
from project.entity.config import TrainingConfig
from project.configeration import ConfigerationManager 
from project.components.callbacks import CallBacks
from project.exception import CustomException
from project.logger import logging
import sys



class Training:
    def __init__(self, config:TrainingConfig):
        """
        Args:
            config: Instance of TrainingConfig containing all training parameters.
        """
        self.config = config
        

    def get_base_model(self):
        """Load and compile the base model."""
        try:
            self.model = tf.keras.models.load_model(self.config.update_base_model)
            self.model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.param_learning_rate),
                loss=tf.keras.losses.CategoricalCrossentropy(),
                metrics=["accuracy"]
            )
        except Exception as e:
            raise CustomException(e, sys)

    def train_valid_generator(self):
        """Create training and validation generators with optional augmentation."""
        # Validation generator
        try:        
            val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                rescale=1./255,
                validation_split=0.2
            )

            self.val_data = val_datagen.flow_from_directory(
                directory=self.config.training_data,
                target_size=self.config.param_image_size[:-1],  # (H, W)
                batch_size=self.config.param_batch_size,
                interpolation="bilinear",
                shuffle=False,
                subset='validation'
            )
        

            # Training generator with optional augmentation
            if self.config.params_augmentation:
                train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                    rescale=1./255,
                    validation_split=0.2,
                rotation_range=40,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                horizontal_flip=True
            )
            else:
                train_datagen = val_datagen

            self.train_data = train_datagen.flow_from_directory(
                directory=self.config.training_data,
                target_size=self.config.param_image_size[:-1],
                batch_size=self.config.param_batch_size,
                interpolation="bilinear",
                shuffle=True,
                subset='training'
            )
        except Exception as e:
            raise CustomException(e, sys)
        

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        """Save the trained model to the given path."""
        model.save(str(path))

    def train(self, callbacks: list = None):
        """
        Train the model using the training and validation generators.

        Args:
            callbacks (list, optional): Keras callbacks for training.
        """
        try:
            # Calculate steps to cover all samples
            steps_per_epoch = math.ceil(self.train_data.samples / self.train_data.batch_size)
            validation_steps = math.ceil(self.val_data.samples / self.val_data.batch_size)

            # Train the model
            history = self.model.fit(
                self.train_data,
                epochs=self.config.param_epochs,
                steps_per_epoch=steps_per_epoch,
                validation_data=self.val_data,
                validation_steps=validation_steps,
                callbacks=callbacks,
                verbose=1
            )

            # Save the trained model
            self.save_model(
                path=self.config.trained_model_path,
                model=self.model
            )

            return history
        except Exception as e:
            raise CustomException(e, sys)   
        

if __name__ == '__main__':
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
