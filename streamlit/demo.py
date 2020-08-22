import streamlit as st
import requests


def extract_entities(text):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = '{{"text":"{}"}}'.format(text)
    # TODO: parametrize url by environment
    response = requests.post('http://localhost:8080/ner/recognize_entities',
                             headers=headers, data=data)
    return response.json()['result']


txt = st.text_area('Text to analyze')

result = extract_entities(txt)

st.write('Entities recognized:')
result_dict = {}
if result:
    for i in result:
        if i[0] in result_dict:
            result_dict[i[0]].append(i[1])
        else:
            result_dict[i[0]] = [i[1]]

    for k, v in result_dict.items():
        st.markdown(f'### {k}')
        for i in v:
            st.write(i)
else:
    st.write('None')
