FROM python:3.11-slim

WORKDIR /nasa_application  

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "nasa_application.wsgi:application", "--bind", "0.0.0.0:8000"]
