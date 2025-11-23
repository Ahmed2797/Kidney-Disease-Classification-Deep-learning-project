from dataclasses import dataclass 
from pathlib import Path 

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class PrepareBasemodelConfig:
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