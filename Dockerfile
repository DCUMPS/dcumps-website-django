# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app/

# migrate database and collect static files
RUN python manage.py migrate
RUN python3 manage.py collectstatic --no-input

# expose port 8000 to the outside world
EXPOSE 8000

# run server
CMD ["gunicorn", "mps.wsgi", "--bind", "0.0.0.0:8000"]