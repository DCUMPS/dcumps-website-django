FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

COPY . /app/

RUN python manage.py collectstatic -v 3 --noinput

#RUN rm -rf /app/mps_site/static

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
