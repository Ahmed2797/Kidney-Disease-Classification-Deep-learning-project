from dataclasses import dataclass 
from pathlib import Path 

@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Dataclass for storing the configuration required to download and extract data.

    Attributes:
        root_dir (Path): Base directory for data artifacts.
        source_url (str): URL from which to download the data.
        local_data_file (Path): Local path where the data will be saved.
        unzip_dir (Path): Directory where the data will be extracted.
    """
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class PrepareBasemodelConfig:
    """
    Dataclass for storing the configuration required to prepare the base model.

    Attributes:
        root_dir (Path): Base directory for base model artifacts.
        base_model (Path): Path to the base model file.
        update_base_model (Path): Path to the updated base model file.
        param_image_size (list): List of image sizes for training.
        param_batch_size (int): Batch size for training.
        param_epochs (int): Number of epochs for training.
    """
    root_dir: Path
    base_model: Path
    update_base_model: Path 
    param_image_size: list
    param_batch_size: int
    param_epochs: int 
    param_learning_rate: float
    param_classics: int
    param_weight:str
    param_include_top: bool


@dataclass(frozen=True)
class PrepareCallbackConfig:
    """
    Dataclass for storing the configuration required to create callbacks.

    Attributes:
        root_dir (Path): Base directory for callback-related artifacts.
        tensorboard_root_log_dir (Path): Directory where TensorBoard logs will be saved.
        checkpoint_model_filepath (Path): Full filepath where the model checkpoint will be stored.
    """
    root_dir: Path
    tensorboard_root_log_dir: Path
    checkpoint_model_filepath: Path


@dataclass(frozen=True)
class TrainingConfig:
    """
    Dataclass for storing the configuration required to train the model.

    Attributes:
        root_dir (Path): Base directory for training artifacts.
        trained_model_path (Path): Path where the trained model will be saved.
        update_base_model (Path): Path to the updated base model file.
        training_data (Path): Path to the training data.
        param_image_size (list): List of image sizes for training.
        param_batch_size (int): Batch size for training.
        param_epochs (int): Number of epochs for training.
    """ 
    root_dir: Path
    trained_model_path: Path
    update_base_model: Path 
    training_data: Path
    param_image_size: list
    param_batch_size: int
    param_epochs: int 
    params_augmentation: bool 
    param_learning_rate: float
