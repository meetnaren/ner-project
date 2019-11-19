from fastapi import APIRouter
from ner.model import NER
from starlette.responses import JSONResponse


router = APIRouter()


@router.post('/extract_name')
def extract_name(input: dict):
    ner = NER()
    result = ner.placeholder_method(input['text'])
    return JSONResponse({'result': result})
