FROM python:3.11-slim

WORKDIR /app

COPY ./ ./

RUN pip3 install -r requirements.txt --no-cache-dir
RUN python manage.py makemigrations users referals

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "referal_system.asgi:application"]  