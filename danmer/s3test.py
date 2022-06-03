# import numpy as np
# loaded_x = np.load('C:\Dev\danmer-backend\danmer\dancedistance_tutortutee.npy')

# print(loaded_x)

# s3 upload test

from __future__ import print_function
import boto3
import os
from dotenv import load_dotenv
load_dotenv()
AWS_S3_ACCESS_KEY_ID = os.getenv('ACCESS_KEY')
AWS_S3_SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
REGION = "ap-northeast-2"
s3 = boto3.client('s3', aws_access_key_id=AWS_S3_ACCESS_KEY_ID, aws_secret_access_key= AWS_S3_SECRET_ACCESS_KEY)
bucket_name = "danmer-videos"
file_name = "C:\Dev\danmer\danmer-backend\danmer\pthread.png"
s3_file_name = "images/p.png"
s3.upload_file(file_name, bucket_name, s3_file_name)
# # s3 download test
# from pathlib import Path

# BASE_DIR = BASE_DIR = Path(__file__).resolve().parent
# local_name =  os.path.join(BASE_DIR,'images/phread.png')
# # images파일이 미리 있어야함
# print(local_name)
# s3.download_file(bucket_name, 'images/phread.png', local_name)


# export ACCESS_KEY = "AKIARDHOONSUZTPRE54F"
# export SECRET_ACCESS_KEY = "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"

def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",# 자신이 설정한 bucket region
            aws_access_key_id="AKIARDHOONSUZTPRE54F",
            aws_secret_access_key= "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"
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3


def s3_put_object(s3, bucket, filepath, access_key):
    """
    s3 bucket에 지정 파일 업로드
    :param s3: 연결된 s3 객체(boto3 client)
    :param bucket: 버킷명
    :param filepath: 파일 위치
    :param access_key: 저장 파일명
    :return: 성공 시 True, 실패 시 False 반환
    """

    s3.upload_file(
        Filename=filepath,
        Bucket=bucket,
        Key=access_key,
    )


s3 = s3_connection()
s3_put_object(s3, "danmer-videos", "C:\Dev\danmer\danmer-backend\danmer\pthread.png", "images/test2.png")


