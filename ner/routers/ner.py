import uuid

from fastapi import APIRouter
from ner.model import NER
from starlette.responses import JSONResponse


router = APIRouter()


@router.post('/extract_name')
def extract_name(input: dict):
    ner = NER(str(uuid.uuid4))
    result = ner.placeholder_method(input['text'])
    ner.store_ner(input['text'], result)
    return JSONResponse({'result': result})
