FROM python:3.7

WORKDIR /code/
COPY . /code/

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8000