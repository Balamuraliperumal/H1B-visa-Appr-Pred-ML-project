from US_Visa.aws_cloud.aws_service import SimpleStorageService
from US_Visa.exception import UsVisaException
from US_Visa.entity.estimator import projectmodel
import sys
from pandas import DataFrame


class UsVisaEstimator:

    def __init__(self,bucket_name,model_path):
        self.bucket_name = bucket_name
        self.model_path = model_path
        self.s3 = SimpleStorageService()
        self.loaded_model:projectmodel=None
    

    def is_model_present(self,model_path):

        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name,s3_key=model_path)
        except UsVisaException as e:
            print(e)
            return False
    
    def load_model(self)->projectmodel:

        return self.s3.load_model(self.model_path,bucket_name=self.bucket_name)
    
    def save_model(self,from_file,remove:bool=False)->None:

        try:
            self.s3.upload_file(from_file,
                                to_filename=self.model_path,
                                bucket_name=self.bucket_name,
                                remove=remove)

        except Exception as e:
            raise UsVisaException(e, sys) from e
    
    def predict(self,data:DataFrame):

        try:
            if self.loaded_model is None:
                self.loaded_model=self.load_model()
            return self.loaded_model.predict(data)
        except Exception as e:
            raise UsVisaException(e, sys)
