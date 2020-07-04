from fastapi import APIRouter
from ner.model import NER
from starlette.responses import JSONResponse
from pydantic import BaseModel


router = APIRouter()


class NameExtractionInput(BaseModel):
    text: str


@router.post('/extract_name')
def extract_name(input: NameExtractionInput) -> JSONResponse:
    ner = NER()
    result = ner.placeholder_method(input.text)
    return JSONResponse({'result': result})
