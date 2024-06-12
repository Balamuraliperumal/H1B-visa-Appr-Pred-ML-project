import os
from US_Visa.constants import DATABASE_NAME,MONGODB_URL_KEY
import pymongo
import certifi

import sys
from US_Visa.exception import UsVisaException
from US_Visa.logger import logging

ca=certifi.where()

class MongoDBClient:

    client=None

    def __init__(self,db_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                db_url=os.getenv(MONGODB_URL_KEY)
                if db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
                MongoDBClient.client=pymongo.MongoClient(db_url,tlsCAFile=ca)
            self.client=MongoDBClient.client
            self.database=self.client[db_name]
            self.db_name=db_name
            logging.info("Connected to MongoDB")
        except Exception as e:
            raise UsVisaException(e,sys)