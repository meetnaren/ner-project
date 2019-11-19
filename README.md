# ner-project

## Contributing to the Project

### Setup

Ensure that you have all dependencies installed by running `pip install -r requirements.txt` AND `pip install -r requirements_dev.txt`. The reason we have two requirements file is because only one is used to build the app. The other contains libraries that are useful for development, but are required in the app itself.

We are using `.env` to manage environment variables. Copy `.env.example` as `.env` and fill the environment variables accordingly.

Lastly, make sure to run `pre-commit install` to enable pre-commit hooks.

## Usage

The FastAPI app is built onto a docker image.

To try the app:

1. Run `docker build . -t ner_app` to build the Docker container
2. Run `docker run -i -p 8080:5000 ner_app` to run the container and expose app on http://localhost:8080

## Testing

For health check:
```
curl 'http://localhost:8080/healthcheck/'
```

To test `extract_name` endpoint:
```
curl 'http://localhost:8080/ner/extract_name' -X POST -H 'Content-Type: application/json' -d '{"text": "text goes here"}'
```
