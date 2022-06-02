# import numpy as np
# loaded_x = np.load('C:\Dev\danmer-backend\danmer\dancedistance_tutortutee.npy')

# print(loaded_x)

# s3 upload test

# from __future__ import print_function
# import boto3
# import os
# from dotenv import load_dotenv
# load_dotenv()

# AWS_S3_ACCESS_KEY_ID = os.getenv('ACCESS_KEY')
# AWS_S3_SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
# REGION = "ap-northeast-2"

# s3 = boto3.client('s3', aws_access_key_id=AWS_S3_ACCESS_KEY_ID, aws_secret_access_key= AWS_S3_SECRET_ACCESS_KEY)
# bucket_name = 'danmer-videos'
# file_name = "C:\Dev\danmer\danmer-backend\danmer\pthread.png"
# s3_file_name = "images/phread.png"
# s3.upload_file(file_name, bucket_name, s3_file_name)

# # s3 download test
# from pathlib import Path

# BASE_DIR = BASE_DIR = Path(__file__).resolve().parent
# local_name =  os.path.join(BASE_DIR,'images/phread.png')
# # images파일이 미리 있어야함
# print(local_name)
# s3.download_file(bucket_name, 'images/phread.png', local_name)

