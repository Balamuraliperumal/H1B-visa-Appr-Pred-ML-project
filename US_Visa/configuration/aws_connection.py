import boto3
import os
from US_Visa.constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_SECRET_ACCESS_KEY_ENV_KEY,REGION_NAME

class  S3Client:

    s3_client = None
    s3_resource = None
    def __init__(self,region_name=REGION_NAME):
        
        if S3Client.s3_resource==None or S3Client.s3_client==None:
            access_key_id=os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            secret_access_key=os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)
            if access_key_id is None:
                raise Exception(f"Environment variable: {AWS_ACCESS_KEY_ID_ENV_KEY} is not set.")
            if secret_access_key is None:
                raise Exception(f"Environment variable: {AWS_SECRET_ACCESS_KEY_ENV_KEY} is not set.")
            

            S3Client.s3_resource=boto3.resource('s3',region_name=region_name,
                                                aws_access_key_id=access_key_id,
                                                aws_secret_access_key=secret_access_key)

            S3Client.s3_client=boto3.client('s3',region_name=region_name,
                                                aws_access_key_id=access_key_id,
                                                aws_secret_access_key=secret_access_key)
        

        self.s3_client = S3Client.s3_client
        self.s3_resource = S3Client.s3_resource