import json
import random
import time
import warnings

import spacy
from spacy.util import compounding, minibatch
from spacy.gold import GoldParse
from spacy.scorer import Scorer
from tqdm import tqdm
import os
import logging
import pandas as pd
import copy

names = pd.read_csv('top100names.csv')


def send_output(text):
    if __name__ == '__main__':
        print(text)
    else:
        logging.info(text)


def get_random_name():
    random_row = names[names['type'] == 'f'].sample(1)
    c = random_row.iloc[0]['country']
    first_name = random_row.iloc[0]['name']
    last_name = names[(names['country'] == c) & (names['type'] == 's')]\
        .sample(1).iloc[0]['name']

    return (first_name, last_name)


def replace_name(data_tuple, first_name, last_name):
    text = data_tuple[0]
    entities = sorted(copy.deepcopy(data_tuple[1]['entities']),
                      key=lambda x: x[0])

    for i in range(len(entities)):
        entity_type = entities[i][2]
        if entity_type == 'FIRST_NAME':
            new_string = first_name
        elif entity_type == 'LAST_NAME':
            new_string = last_name
        else:
            continue
        old_string_len = entities[i][1] - entities[i][0]
        new_string_len = len(new_string)
        diff = new_string_len - old_string_len
        text = text[:entities[i][0]] + new_string + text[entities[i][1]:]
        entities[i][1] = entities[i][0] + new_string_len
        if i < len(entities) - 1:
            for j in range(i+1, len(entities)):
                entities[j][0] += diff
                entities[j][1] += diff
    try:
        for i in range(len(entities)):
            if entities[i][2] == 'FIRST_NAME':
                assert text[entities[i][0]:entities[i][1]] == first_name
            elif entities[i][2] == 'LAST_NAME':
                assert text[entities[i][0]:entities[i][1]] == last_name
    except AssertionError:
        send_output(data_tuple)
        send_output(first_name, last_name)
        send_output(text)
        send_output(entities)
        raise AssertionError
    return (text.lower(), {'entities': entities})


def get_train_data(labels, data_aug_factor):
    with open('dump.json', 'r') as f:
        dump = json.loads(f.read())

    data_dump = dump['data']
    data = []

    for c, v in tqdm(data_dump.items()):
        data_tuple = (v['text'].lower(), {'entities': []})
        if v['entities']:
            if any([i in [e[2] for e in v['entities']] for i in labels]):
                for e in v['entities']:
                    if e[2] in labels:
                        data_tuple[1]['entities'].append(e)
                data.append(data_tuple)
                for i in range(data_aug_factor):
                    data.append(replace_name(data_tuple, *(get_random_name())))

    send_output(f'{len(data)} records added.')

    return data


def evaluate(ner_model, examples):
    scorer = Scorer()
    for input_, annot in examples:
        doc_gold_text = ner_model.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities=annot['entities'])
        pred_value = ner_model(input_)
        scorer.score(pred_value, gold)
    return scorer.scores


def main(model='latest', n_iter=10):
    # model: 'latest' to retrieve the latest model from the Models directory,
    # 'blank' to train a blank model from scratch
    # n_iter: no. of iterations to train the model
    LABELS = [
        'FIRST_NAME',
        'LAST_NAME'
    ]

    TRAIN_VAL_SPLIT = 0.80
    DATA_AUGMENTATION_FACTOR = 25

    DATA = get_train_data(LABELS, DATA_AUGMENTATION_FACTOR)
    num_records = len(DATA)

    if model.lower() == 'blank':
        nlp = spacy.blank('en')  # create blank Language class
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
    else:
        latest_model = max([d for d in os.listdir('Models')])
        nlp = spacy.load('Models/'+latest_model)
        send_output(f'Loaded model {latest_model}')
        ner = nlp.get_pipe('ner')

    for label in LABELS:
        ner.add_label(label)

    if model.lower() == 'blank':
        optimizer = nlp.begin_training()
    else:
        optimizer = nlp.entity.create_optimizer()

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

    with nlp.disable_pipes(*other_pipes) and warnings.catch_warnings():
        # show warnings for misaligned entity spans once
        warnings.filterwarnings('ignore', category=UserWarning, module='spacy')

        sizes = compounding(1.0, 4.0, 1.001)
        # batch up the examples using spaCy's minibatch
        for itn in range(n_iter):
            send_output(f'In iteration {itn + 1}')
            random.shuffle(DATA)
            TRAIN_DATA = DATA[:int(TRAIN_VAL_SPLIT * num_records)]
            VALID_DATA = DATA[len(TRAIN_DATA):]
            send_output(f'Training on {len(TRAIN_DATA)} records, \
                validating on {len(VALID_DATA)} records.')

            batches = minibatch(TRAIN_DATA, size=sizes)
            losses = {}
            for batch in tqdm(batches):
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.35,
                           losses=losses)
            send_output('Training losses: ' + str(losses))
            scores = evaluate(nlp, VALID_DATA)
            send_output(scores)

    # test the trained model
    test_text = 'The name of my mentor is Mandy Gu'
    doc = nlp(test_text)
    send_output(f'Entities in {test_text}')
    for ent in doc.ents:
        send_output(ent.label_ + ' ' + ent.text)

    # save the trained model
    model_name = 'model_' + time.strftime('%Y%m%d-%H%M%S')
    nlp.meta['name'] = model_name
    nlp.meta['author'] = 'Naren Santhanam'
    nlp.meta['email'] = 'meetnaren@gmail.com'
    nlp.to_disk(f'Models/{model_name}')


if __name__ == '__main__':
    main()
