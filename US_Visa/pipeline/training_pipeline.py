import sys

from US_Visa.logger import logging

from US_Visa.exception import UsVisaException

from US_Visa.components.data_ingestion import DataIngestion
from US_Visa.components.data_validation import DataValidation
from US_Visa.components.data_transformation import DataTransformation
from US_Visa.components.model_trainer import ModelTrainer


from US_Visa.entity.config_entity import (DataIngestionConfig,
                                          DataValidationConfig,
                                          DataTransformationConfig,
                                          ModelTrainerConfig)

from US_Visa.entity.artifact_entity import (DataIngestionArtifact,
                                            DataValidationArtifact,
                                            DataTransformationArtifact,
                                            ModelTrainerArtifact)


class TrainPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()


    def start_data_ingestion(self) -> DataIngestionArtifact:

        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Got the data from Mongodb")
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Train and Test set created from Mongodb dataset")
            logging.info("Start_data_ingestion method of TrainPipeline class completed")

            return data_ingestion_artifact
        except Exception as e:
            raise UsVisaException(e, sys) from e
    

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        
        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                            data_validation_config = self.data_validation_config
                                            )
            
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation on the dataset")

            logging.info("Completed the start_data_validation method of TrainPipeline class")

            return data_validation_artifact
        except Exception as e:
            raise UsVisaException(e, sys) from e


    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact,data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:

        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                    data_validation_artifact=data_validation_artifact,
                                                    data_transformation_config = self.data_transformation_config
                                                    )
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise UsVisaException(e, sys)
        

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:

        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                        model_trainer_config = self.model_trainer_config
                                        )
            
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise UsVisaException(e, sys) from e

    def run_pipeline(self) -> None:

        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

        except Exception as e:
            raise UsVisaException(e, sys) from e
