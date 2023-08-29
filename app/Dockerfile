# root builder stage
FROM python:3.9-slim AS builder
WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt


# test stage
FROM builder AS test
COPY ./requirements.test.txt ./
RUN pip install --no-cache-dir -r ./requirements.test.txt
COPY ./main.py ./
COPY ./anonymizer ./anonymizer
COPY ./tests ./tests
RUN pytest -v tests/

# prod stage
FROM builder AS prod
COPY ./main.py ./
COPY ./anonymizer ./anonymizer
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python3", "/usr/src/app/main.py"]
