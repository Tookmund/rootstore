ARG PYTHON_VERSION=3.9-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pipenv install --deploy --system

COPY . /code

#RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "--timeout", "120", "rootstore.wsgi"]
