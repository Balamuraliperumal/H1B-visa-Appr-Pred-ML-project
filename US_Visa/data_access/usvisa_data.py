from US_Visa.configuration.mongo_db import MongoDBClient
from US_Visa.constants import DATABASE_NAME
from US_Visa.exception import UsVisaException
import pandas as pd
import sys
from typing import Optional
import numpy as np

class UsVisaData:
     
    """
    This class helps to export the data from mongo db records as a dataframe
    """
    
    def __init__(self):
        
        try:
            self.mongo_client = MongoDBClient(db_name=DATABASE_NAME)
        except Exception as e:    
            raise UsVisaException(e,sys)

    def export_data(self,collection_name:str,database_name:Optional[str]=None)->pd.DataFrame:
        try:

            if database_name is None:
                collection=self.mongo_client.database[collection_name]
            else:
                collection=self.mongo_client[database_name][collection_name]

            records = collection.find()
            df = pd.DataFrame(list(records))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)
            return df
        except Exception as e:
            raise UsVisaException(e,sys)