# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
EXPOSE 8000
WORKDIR /app 
#COPY requirements.txt /app
#RUN pip3 install -r requirements.txt --no-cache-dir
RUN pip3 install django bs4 requests html5lib feedparser yt_dlp datetime pandas django-embed-video whitenoise pillow --no-cache-dir
COPY . /app 
ENTRYPOINT ["python3"] 
WORKDIR /app
RUN python3 ./mps/manage.py collectstatic -v 2 --noinput
COPY . /app
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

FROM builder as dev-envs
RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
CMD ["manage.py", "runserver", "0.0.0.0:8000"]