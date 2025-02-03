FROM python:3.12-slim

ENV DOCKER=1

WORKDIR "/app"

COPY ConfigurationFile.py .
COPY LetterboxdTweeter.py .
COPY Tweet.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-u", "LetterboxdTweeter.py"]