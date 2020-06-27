import pandas as pd
from sqlalchemy.orm import sessionmaker
import logging

from ner import settings
from ner.db import DB

print(settings.env)

def extract_entities(input_text):
    # get latest model
    latest_model = max([d for d in os.listdir('Models')])
    nlp = spacy.load('Models/'+latest_model)
    logging.debug(f'Loaded model {latest_model}')

    # apply latest model on input text
    doc = nlp(input_text)

    # return the entities and texts
    result = [(ent.label_, ent.text) for ent in doc.ents] 
    return result


class NER:
    @staticmethod
    def load_data(sql):
        sessionmaker(bind=DB.create_db_engine(), autocommit=True)
        return pd.read_sql_query(sql, con=DB.create_db_engine())

    def placeholder_method(self, text):
        return text
