from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_HOST = getenv("DB_HOST")
DB_PSWD = getenv("DB_PSWD")
SENDGRID_API_KEY = getenv("SENDGRID_API_KEY")