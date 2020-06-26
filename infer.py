import os
import spacy
import logging

def main(input_text):
    # get latest model
    latest_model = max([d for d in os.listdir('Models')])
    nlp = spacy.load('Models/'+latest_model)
    logging.debug(f'Loaded model {latest_model}')

    # apply latest model on input text
    doc = nlp(input_text)

    # return the entities and texts
    result = []
    for ent in doc.ents:
        result.append((ent.label_, ent.text))
    
    return result