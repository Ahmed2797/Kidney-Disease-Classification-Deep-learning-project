import os
import sys
import json
import yaml
import base64
import joblib

from pathlib import Path
from typing import Any, List

from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations

from project.logger import logging
from project.exception import CustomException


# ============================
# Y A M L   F U N C T I O N S
# ============================

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Read a YAML file and return its content as ConfigBox."""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)

        if content is None:
            raise CustomException("YAML file is empty.", None)

        logging.info(f"YAML file loaded successfully: {path_to_yaml}")
        return ConfigBox(content)

    except yaml.YAMLError as e:
        raise CustomException(f"Invalid YAML syntax in: {path_to_yaml}", e)

    except BoxValueError as e:
        raise CustomException("YAML content cannot be converted into ConfigBox.", e)

    except Exception as e:
        raise CustomException(e, sys)


# ====================================
# D I R E C T O R I E S   H A N D L I N G
# ====================================

# @ensure_annotations
# def create_directories(path_to_directories: list, verbose=True):
#     """create list of directories

#     Args:
#         path_to_directories (list): list of path of directories
#         ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
#     """
#     for path in path_to_directories:
#         os.makedirs(path, exist_ok=True)
#         if verbose:
#             logging.info(f"created directory at: {path}")


@ensure_annotations
def create_directories(path):
    """Create directories."""
    try:
        if isinstance(path, list):
            for p in path:
                os.makedirs(p, exist_ok=True)
        else:
            os.makedirs(path, exist_ok=True)
    except Exception as e:
         raise CustomException(e, e)





# =============================
# J S O N   F U N C T I O N S
# =============================

@ensure_annotations
def save_json(path: Path, data: dict):
    """Save a dictionary as a JSON file."""
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"JSON file saved at: {path}")

    except Exception as e:
        raise CustomException(e, sys)


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load a JSON file and return ConfigBox."""
    try:
        with open(path) as f:
            content = json.load(f)

        logging.info(f"JSON file loaded successfully: {path}")
        return ConfigBox(content)

    except Exception as e:
        raise CustomException(e, sys)


# ===============================
# B I N A R Y   F U N C T I O N S
# ===============================

@ensure_annotations
def save_bin(data: Any, path: Path):
    """Save binary data using joblib."""
    try:
        joblib.dump(value=data, filename=path)
        logging.info(f"Binary file saved at: {path}")
    except Exception as e:
        raise CustomException(e, sys)


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Load binary data using joblib."""
    try:
        data = joblib.load(path)
        logging.info(f"Binary file loaded from: {path}")
        return data
    except Exception as e:
        raise CustomException(e, sys)


# ==================
# U T I L I T Y
# ==================

@ensure_annotations
def get_size(path: Path) -> str:
    """Return file size in KB."""
    try:
        size_in_kb = round(os.path.getsize(path) / 1024)
        return f"~ {size_in_kb} KB"
    except Exception as e:
        raise CustomException(e, sys)


# =================================
# B A S E 6 4   E N C O D E / D E C O D E
# =================================

@ensure_annotations
def decodeImage(imgstring: str, fileName: str) -> None:
    """Decode a Base64 string and save as an image."""
    try:
        imgdata = base64.b64decode(imgstring)
        with open(Path(fileName), 'wb') as f:
            f.write(imgdata)

        logging.info(f"Image decoded and saved: {fileName}")

    except Exception as e:
        raise CustomException(e, sys)


@ensure_annotations
def encodeImageIntoBase64(croppedImagePath: str) -> bytes:
    """Encode an image file into Base64."""
    try:
        with open(Path(croppedImagePath), "rb") as f:
            return base64.b64encode(f.read())
    except Exception as e:
        raise CustomException(e, sys)


