import tensorflow as tf
from project.entity.config import PrepareBasemodelConfig
from pathlib import Path 




class PrepareBaseModel:
    def __init__(self,config=PrepareBasemodelConfig):
        self.config = config
    
    def get_base_model(self):
        self.model = tf.keras.applications.VGG16(
        include_top=self.config.param_include_top,
        weights=self.config.param_weight,
        input_shape=self.config.param_image_size,
        classes=self.config.param_classics,
        classifier_activation='softmax'
        )

        self.save_model(self.config.base_model,model=self.model)

    def update_base_model(self):
        self.full_model = self.prepare_model_layers(
            model=self.model,
            num_classes=self.config.param_classics,
            freeze_all=True, # base model freeze
            freeze_till=None, # classifier unfreeze
            learning_rate = self.config.param_learning_rate
        )
        self.save_model(self.config.update_base_model,model=self.full_model)



    @staticmethod
    def save_model(file_path:Path,model:tf.keras.Model):
        model.save(file_path)

    @staticmethod
    def prepare_model_layers(model,num_classes,learning_rate, freeze_all=False, freeze_till=None):
        """
        Freeze layers of a TensorFlow/Keras model based on configuration.

        Args:
            model (tf.keras.Model): The model whose layers need to be frozen.
            freeze_all (bool): If True, all layers will be frozen (trainable=False).
            freeze_till (int or None): 
                Number of layers from the end that should remain trainable.
                Example: freeze_till=10 → freeze all layers except the last 10.

        Returns:
            tf.keras.Model: The model with updated layer trainable settings.
        """

        # Freeze all layers
        if freeze_all:
            for layer in model.layers:
                layer.trainable = False

        # Freeze layers up to a certain point
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                layer.trainable = False

        flatten_in = tf.keras.layers.Flatten()(model.output)
        prediction = tf.keras.layers.Dense(num_classes, activation='softmax')(flatten_in)

        # Combine base model and new classifier
        full_model = tf.keras.Model(inputs=model.input, outputs=prediction)
        full_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss=tf.keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"]
        )

        full_model.summary()

        return full_model

