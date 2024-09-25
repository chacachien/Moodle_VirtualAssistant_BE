# FROM alpine

# # Install Python and build tools
# RUN apk update && apk add python3~3.12 g++ build-base

FROM python:3.12.6-slim-bullseye@sha256:7915f3eaac1cb92b7472700412ab78f1dd73f97ba344ae9064e181a44ca2a9b3
#RUN apk update && apk add --no-cache g++ build-base
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /code
ENV PROJECT_NAME="VIRTUAL ASSISTANT"
ENV DATABASE_URL="mysql+mysqlconnector://moodleuser:password123@localhost/moodle"
ENV POSTGRES_SERVER="moodle.cd2wy4iagdv9.ap-southeast-1.rds.amazonaws.com"
ENV POSTGRES_DB="moodle"
ENV POSTGRES_USER="postgres"
ENV POSTGRES_PASSWORD="1307x2Npk"
ENV POSTGRES_PORT="5432"
ENV HUGGINGFACE_API_KEY="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"
ENV PINECONE_API_KEY="3e9197b0-4ce5-4702-b779-e955674bdbb0"
ENV GOOGLE_API_KEY="AIzaSyAqUcIWqH_CO2S-ayPm7YgW4Jk5ffCww2E"
ENV GROQ_API_KEY="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"
ENV OPENAI_API_KEY="NO"
ENV LANGCHAIN_TRACING_V2="true"
ENV LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
ENV LANGCHAIN_API_KEY="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"
ENV LANGCHAIN_PROJECT="va"

RUN python3 -m venv venv 
RUN venv/bin/pip install -U pip setuptools wheel 
RUN venv/bin/pip install poetry==1.8.0
# RUN venv/bin/pip install --no-binary grpcio grpcio==1.65.1

# RUN . venv/bin/activate && \
#     pip install poetry==1.7.0
    #pip install --upgrade pip setuptools wheel
    # pip install grpcio --no-binary :all:

COPY pyproject.toml /code/

RUN . venv/bin/activate && \
    poetry install
COPY . /code

EXPOSE 5000
CMD ["venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
