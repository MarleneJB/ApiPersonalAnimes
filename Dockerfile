FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /animesapi
WORKDIR /animesapi
COPY requeriments.txt /animesapi/
RUN pip install -r requeriments.txt
COPY . /animesapi/
CMD python manage.py runserver 0.0.0.0:8080
