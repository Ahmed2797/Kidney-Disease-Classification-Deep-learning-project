import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from project.components.model_evalution import Evaluation
from project.configeration import ConfigerationManager
from project.exception import CustomException



class ModelEvaluationPipeline:
    def __init__(self):
        pass
    def main(self):
        try:
            config = ConfigerationManager()
            model_evaluation_config = config.get_model_evaluation_config()

            evaluation = Evaluation(config=model_evaluation_config)
            evaluation.save_outputs()
            evaluation.log_mlflow()
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    try:
        pipeline = ModelEvaluationPipeline()
        pipeline.main()
    except Exception as e:
        raise CustomException(e, sys)
