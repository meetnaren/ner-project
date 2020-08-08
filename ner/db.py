import os

from sqlalchemy import create_engine


class DB:
    @classmethod
    def create_db_engine(self):
        conn = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{schema}'.format(  # noqa
            user=os.environ.get('user'),
            password=os.environ.get('password'),
            host=os.environ.get('host'),
            port=os.environ.get('port'),
            schema=os.environ.get('database')
        )

        engine = create_engine(conn)
        return engine
