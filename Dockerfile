FROM python:3.9.1-slim-buster

LABEL org.opencontainers.image.source https://github.com/nownabe/discord-tts

RUN mkdir -p /app \
  && apt-get update \
  && apt-get install -y --no-install-recommends ffmpeg=7:4.1.6-1~deb10u1 \
  && pip install pipenv==2020.11.15 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --deploy --system

COPY . /app

CMD ["python", "main.py"]
