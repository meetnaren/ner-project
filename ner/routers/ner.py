from fastapi import APIRouter
from ner.model import extract_entities
from starlette.responses import JSONResponse

router = APIRouter()


@router.post('/recognize_entities')
def recognize_entities(input: dict):
    result = extract_entities(input['text'])
    return JSONResponse({'result': result})
