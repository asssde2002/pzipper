FROM python:3.13
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y postgresql-client
WORKDIR /code
COPY ./backend/requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./backend/ /code/