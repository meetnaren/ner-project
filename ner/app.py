from fastapi import FastAPI
from ner.routers import ner

app = FastAPI()
app.include_router(ner.router, prefix='/ner')


@app.get('/healthcheck', status_code=200)
async def healthcheck():
    return 'the app is healthy'
