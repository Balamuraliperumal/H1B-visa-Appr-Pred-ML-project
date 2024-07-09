import sys

from US_Visa.aws_cloud.aws_service import SimpleStorageService
from US_Visa.exception import UsVisaException
from US_Visa.logger import logging
from US_Visa.entity.artifact_entity import ModelPusherArtifact,ModelEvaluationArtifact
from US_Visa.entity.config_entity import ModelPusherConfig
from US_Visa.entity.s3_estimator import UsVisaEstimator


class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact,
                 model_pusher_config: ModelPusherConfig):
        
        self.s3 = SimpleStorageService()
        self.model_evalution_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.visa_estimator = UsVisaEstimator(bucket_name=model_pusher_config.bucket_name,
                                              model_path=model_pusher_config.s3_model_key_path)
        
    
    def initiate_model_pusher(self) -> ModelPusherArtifact:

        logging.info("Entered initiate_model_pusher method of ModelTrainer class")

        try:
            logging.info("uploading artifacts folder to s3 bucket")

            self.visa_estimator.save_model(from_file=self.model_evalution_artifact.trained_model_path)

            model_pusher_artifact = ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,
                                                        s3_model_path=self.model_pusher_config.s3_model_key_path)
            
            logging.info("Uploaded artifacts folder to s3 bucket")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")

            return model_pusher_artifact
        except Exception as e:
            raise UsVisaException(e, sys) from e