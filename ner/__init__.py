import os
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        load_dotenv('.env')
        self.env = self.get_env()

    def get_env(self):
        return os.environ.get('environment')


settings = Settings()
