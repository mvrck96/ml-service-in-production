ARG DOCKERFILE_BUILD_IMAGE="python"
ARG DOCKERFILE_BUILD_TAG="3.8-slim-buster"

FROM $DOCKERFILE_BUILD_IMAGE:$DOCKERFILE_BUILD_TAG
ARG APP_NAME=${APP_NAME:-ds-service-template}

WORKDIR /ds-service-template
RUN python -m venv /$APP_NAME/.venv
ENV PATH "/$APP_NAME/.venv/bin:$PATH"

COPY requirements.txt .

COPY /src ./src/
COPY main.py .

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn main:app --worker-class uvicorn.workers.UvicornWorker\
    --workers 4\
    --bind 0.0.0.0:8000
