import json
import random
import time
import warnings

import spacy
from spacy.util import compounding, minibatch
from spacy.gold import GoldParse
from spacy.scorer import Scorer
from tqdm import tqdm
import plac
import os

def get_train_data(labels):
    with open('dump.json', 'r') as f:
        dump = json.loads(f.read())

    data_dump = dump['data']
    DATA = []

    for c, v in data_dump.items():
        data_tuple = (v['text'], {'entities':[]})
        if v['entities']:
            if any([i in [e[2] for e in v['entities']] for i in labels]):
                for e in v['entities']:
                    if e[2] in labels:
                        data_tuple[1]['entities'].append(e)
                DATA.append(data_tuple)
    print(f'{len(DATA)} records added.')
    return DATA

def evaluate(ner_model, examples):
    scorer = Scorer()
    for input_, annot in examples:
        #print(input_, annot)
        doc_gold_text = ner_model.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities=annot['entities'])
        pred_value = ner_model(input_)
        scorer.score(pred_value, gold)
    return scorer.scores

@plac.annotations(
    model=("'blank' or 'latest'", 'option', 'm'),
    n_iter=('No. of training iterations', 'option', 'n')
)
def main(model='blank', n_iter=1):

    LABELS = [
        'FIRST_NAME',
        'LAST_NAME'
    ]

    TRAIN_VAL_SPLIT = 0.80

    DATA = get_train_data(LABELS)
    num_records = len(DATA)

    if model.lower() == 'blank':
        nlp = spacy.blank('en')  # create blank Language class
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    else:
        latest_model = max([d for d in os.listdir('Models')])
        nlp = spacy.load('Models/'+latest_model)
        print(f'Loaded model {latest_model}')
        ner = nlp.get_pipe('ner')

    for label in LABELS:
        ner.add_label(label)

    if model.lower() == 'blank':
        optimizer = nlp.begin_training()
    else:
        optimizer = nlp.entity.create_optimizer()

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

    with nlp.disable_pipes(*other_pipes) and warnings.catch_warnings():
        #show warnings for misaligned entity spans once
        warnings.filterwarnings("once", category=UserWarning, module='spacy')

        sizes = compounding(1.0, 4.0, 1.001)
        # batch up the examples using spaCy's minibatch
        for itn in range(n_iter):
            print(f'In iteration {itn + 1}')
            random.shuffle(DATA)
            TRAIN_DATA = DATA[:int(TRAIN_VAL_SPLIT * num_records)]
            VALID_DATA = DATA[len(TRAIN_DATA):]
            print(f'Training on {len(TRAIN_DATA)} records, validating on {len(VALID_DATA)} records.')

            batches = minibatch(TRAIN_DATA, size=sizes)
            losses = {}
            for batch in tqdm(batches):
                #print(f'Batch {n} in progress...')
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
            print("Training losses:", losses)
            scores = evaluate(nlp, VALID_DATA)
            print(scores)

        
    # test the trained model
    test_text = "The name of my mentor is Mandy Gu"
    doc = nlp(test_text)
    print(f'Entities in {test_text}')
    for ent in doc.ents:
        print(ent.label_, ent.text)

    #save the trained model
    model_name = 'model_' + time.strftime("%Y%m%d-%H%M%S")
    nlp.meta['name'] = model_name
    nlp.meta['author'] = 'Naren Santhanam'
    nlp.meta['email'] = 'meetnaren@gmail.com'
    nlp.to_disk(f'Models/{model_name}')

if __name__ == '__main__':
    plac.call(main)