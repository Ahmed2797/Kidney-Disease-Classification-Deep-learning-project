
import tensorflow as tf
import numpy as np
import os



class ImagePredictor:
    """
    A utility class for kidney disease image classification using a trained Keras model.

    This class loads a saved model, preprocesses CT scan images, and returns
    predictions with confidence scores.

    Attributes:
        model (tf.keras.Model): The loaded deep learning model.
    """

    def __init__(self, model_path: str):
        """
        Initialize the ImagePredictor by loading the trained model.

        Args:
            model_path (str): Path to the saved Keras model (.h5 or .keras file).

        Raises:
            FileNotFoundError: If the model file does not exist.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        self.model = tf.keras.models.load_model(model_path)

    def preprocess_image(self, img_path: str, target_size=(224, 224)):
        """
        Load and preprocess an image for model prediction.

        Steps:
        - Load image and resize to target size
        - Convert to numpy array
        - Expand batch dimension
        - Normalize pixel values to [0, 1]

        Args:
            img_path (str): Path to the input image.
            target_size (tuple): Resize target (height, width).

        Returns:
            np.ndarray: Preprocessed image ready for prediction.

        Raises:
            FileNotFoundError: If the image file does not exist.
        """
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image file not found at {img_path}")

        img = tf.keras.utils.load_img(img_path, target_size=target_size)
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # normalize

        return img_array

    def predict(self, img_path: str):
        """
        Predict whether the input CT image indicates kidney tumor or normal.

        Args:
            img_path (str): Path to the image file.

        Returns:
            tuple:
                - str: Prediction label ("Kidney Disease Detected : Tumor" or "Normal")
                - float: Confidence score (0-1)

        Notes:
            Assumes class index 1 = Tumor, 0 = Normal.
        """
        img_array = self.preprocess_image(img_path)
        predictions = self.model.predict(img_array)
        label = "Tumor" if np.argmax(predictions) == 1 else "Normal"
        confidence = float(np.max(predictions))

        return label, confidence