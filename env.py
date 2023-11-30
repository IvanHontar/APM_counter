import os
from dotenv import load_dotenv


load_dotenv()


DB_HOST = os.environ.get('db_host')
DB_NAME = os.environ.get('db_name')
DB_USER = os.environ.get('db_user')
DB_PASSWORD = os.environ.get('db_password')