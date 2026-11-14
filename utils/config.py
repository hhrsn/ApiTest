import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    API_USER = os.getenv("API_USER", "emilys")
    API_PASSWORD = os.getenv("API_PASSWORD", "emilyspass")


config = Config()
