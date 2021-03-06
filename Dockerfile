FROM python:3.7-slim-buster
LABEL maintainer="Naren"

RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /usr/src/ner
WORKDIR /usr/src/ner

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN python3 -m spacy download en

COPY . .

EXPOSE 5000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "ner.app:app"]
