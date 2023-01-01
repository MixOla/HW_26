FROM python:3.10-slim

ENV HOME /app
WORKDIR $HOME

COPY requirements.txt .
RUN python3 -m pip install --no-cache -r requirements.txt

COPY flask_app/ .

ENTRYPOINT ["sh", "entrypoint.sh"]