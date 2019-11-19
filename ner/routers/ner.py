from fastapi import APIRouter
from ner.model import NER


router = APIRouter()


@router.post('/extract_name')
def extract_name(text):
    ner = NER()
    return ner.placeholder_method(text)
