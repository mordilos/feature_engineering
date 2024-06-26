FROM python:3.9
LABEL authors="nektariospatlakas"

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
