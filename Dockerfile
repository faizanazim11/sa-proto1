FROM python:3.11.4-slim-bookworm
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
WORKDIR /code
RUN apt update && apt install curl -y
COPY . /code
CMD [ "python", "app.py" ]
