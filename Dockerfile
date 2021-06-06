# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1

ENV VIRTUAL_ENV=/ve
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY . /LotDividerAPI/
WORKDIR /LotDividerAPI
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ['python manage.py runserver', '0.0.0.0:8000']