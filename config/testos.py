from dotenv import load_dotenv
import os

load_dotenv()
print(type(os.getenv('SECRET_ACCESS_KEY')))
print(type(os.environ.get('ACCESS_KEY')))
