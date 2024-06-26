import os
import sys
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from US_Visa.entity.config_entity import DataIngestionConfig
from US_Visa.entity.artifact_entity import DataIngestionArtifact
from US_Visa.exception import UsVisaException
from US_Visa.logger import logging
from US_Visa.data_access.usvisa_data import UsVisaData

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):

        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise UsVisaException(e,sys)
    
    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export data into feature store
        """
        try:
            logging.info("Exporting the data from mongodb")
            us_visa_data = UsVisaData()
            df = us_visa_data.export_data(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Shape of df : {df.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving exported date from mongodb into feature store file path: {feature_store_file_path}")
            df.to_csv(feature_store_file_path, index=False,header=True)
            return df
        except Exception as e:
            raise UsVisaException(e, sys)
    
   
    def split_data_train_test(self,df:DataFrame) ->None:
        
        logging.info("Started split_data_train_test method of Data_Ingestion class")

        try:
            train_set,test_set = train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Train test split completed")
            logging.info("Exited split_data_train_test method of Data_Ingestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logging.info("Export of train and test file Completed")
        except Exception as e:
            raise UsVisaException(e, sys)


    def initiate_data_ingestion(self) -> DataIngestionArtifact:

        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            dataframe = self.export_data_into_feature_store()

            logging.info("got the data from mongodb")

            self.split_data_train_test(dataframe)

            logging.info("Train test split completed on the dataset")

            logging.info("Exited initiate_data_ingestion method of Data_ingestion class")

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact
        except Exception as e:
            raise UsVisaException(e, sys) from e