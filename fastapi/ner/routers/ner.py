from fastapi import APIRouter

from ner.model import extract_entities
from starlette.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()


class NameExtractionInput(BaseModel):
    text: str


@router.post('/recognize_entities')
def recognize_entities(input: NameExtractionInput) -> JSONResponse:
    result = extract_entities(input['text'])
    return JSONResponse({'result': result})
