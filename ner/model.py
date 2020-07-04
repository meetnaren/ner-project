import datetime
import pandas as pd

from sqlalchemy.orm import sessionmaker

from ner.db import DB
from ner.datawarehouse.tables import ExtractedEntities


class NER:
    def __init__(self, id):
        session = sessionmaker(bind=DB.create_db_engine())
        self.id = id
        self.session = session()
        self.created_at = datetime.datetime.today().date()

    @staticmethod
    def load_data(sql):
        sessionmaker(bind=DB.create_db_engine(), autocommit=True)
        return pd.read_sql_query(sql, con=DB.create_db_engine())

    def placeholder_method(self, text):
        return text

    def store_ner(self, text, entities):
        ner = ExtractedEntities(
                id=self.id,
                created_at=self.created_at,
                text=text,
                entities=entities)
        self.session.add(ner)
        self.session.commit()

    def close_session(self):
        self.session.close()
