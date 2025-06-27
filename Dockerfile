FROM python:3.13.5-alpine
WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]