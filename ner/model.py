import pandas as pd
from sqlalchemy.orm import sessionmaker

from ner import settings
from ner.db import DB

print(settings.env)


class Model:
    @staticmethod
    def load_data(sql):
        sessionmaker(bind=DB.create_db_engine(), autocommit=True)
        return pd.read_sql_query(sql, con=DB.create_db_engine())
