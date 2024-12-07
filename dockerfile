# Dockerfile
FROM python:3.11-slim

WORKDIR /nasa_application 

COPY . /nasa_application 

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "nasa_application.wsgi:application", "--bind", "0.0.0.0:8000"]
