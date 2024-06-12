import sys

from US_Visa.logger import logging

from US_Visa.exception import UsVisaException

from US_Visa.components.data_ingestion import DataIngestion

from US_Visa.entity.config_entity import (DataIngestionConfig)

from US_Visa.entity.artifact_entity import (DataIngestionArtifact)


class TrainPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()


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
    
    def run_pipeline(self) -> None:

        try:
            data_ingestion_artifact = self.start_data_ingestion()

        except Exception as e:
            raise UsVisaException(e, sys) from e
