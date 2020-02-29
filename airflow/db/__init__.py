import os

from sqlalchemy import create_engine


class Settings:
    def __init__(self):
        self.env = os.environ.get('env')


class DB:
    @classmethod
    def create_engine(self):
        conn = 'postgresql://{user}:{password}@{host}:{port}/{schema}'.format(  # noqa
            user=os.environ.get('db_user'),
            password=os.environ.get('db_password'),
            host=os.environ.get('db_host'),
            port=os.environ.get('db_port'),
            schema=os.environ.get('db_database')
        )

        engine = create_engine(conn)
        return engine


settings = Settings()
