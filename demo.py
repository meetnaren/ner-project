import streamlit as st
from ner.model import extract_entities

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
