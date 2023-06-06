FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /ApiPersonalAnimes
WORKDIR /ApiPersonalAnimes
COPY requeriments.txt /ApiPersonalAnimes/
RUN pip install -r requeriments.txt
COPY . /ApiPersonalAnimes/
CMD python manage.py runserver 0.0.0.0:8080
