FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

RUN pip install uv

RUN uv pip install --system --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic -v 3 --noinput

EXPOSE 8000

CMD ["gunicorn", "mps.wsgi:application", "--bind", "0.0.0.0:8000"]
