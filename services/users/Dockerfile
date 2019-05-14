FROM python:3.7.2-alpine
WORKDIR /usr/sr/app
COPY ./requirements.txt /usr/sr/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/sr/app
CMD python manage.py run -h 0.0.0.0