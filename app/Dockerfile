FROM python:3.8-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y

EXPOSE 5000
# EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN pip install --upgrade pip
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["flask", "run"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

