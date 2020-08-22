import logging
import os
import spacy


def extract_entities(input_text=''):
    models_dir = os.path.join('..', 'Models')
    latest_model = max([d for d in os.listdir(models_dir)])
    latest_model_path = os.path.join(models_dir, latest_model)
    nlp = spacy.load(latest_model_path)
    logging.info(f'Loaded model {latest_model}')

    doc = nlp(input_text.lower())

    return [(ent.label_, ent.text) for ent in doc.ents]
