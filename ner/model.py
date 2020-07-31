import pandas as pd
from sqlalchemy.orm import sessionmaker
import logging
import os
import spacy

#from ner import settings
#from ner.db import DB

#print(settings.env)

def extract_entities(input_text=''):
    # get latest model
    models_dir = os.path.join('..', 'Models') if __name__ == '__main__' else 'Models'
    latest_model = max([d for d in os.listdir(models_dir)])
    latest_model_path = os.path.join(models_dir, latest_model)
    nlp = spacy.load(latest_model_path)
    print(f'Loaded model {latest_model}')

    doc = nlp(input_text.lower())

    # return the entities and texts
    return [(ent.label_, ent.text) for ent in doc.ents]

class NER:
    @staticmethod
    def load_data(sql):
        sessionmaker(bind=DB.create_db_engine(), autocommit=True)
        return pd.read_sql_query(sql, con=DB.create_db_engine())

    def placeholder_method(self, text):
        return text

if __name__ == '__main__':
    extract_entities(input('Enter text with entities to be recognized:'))