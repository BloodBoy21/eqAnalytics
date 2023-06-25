FROM python:3.10

# Path: /app
WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

CMD ["python", "main.py"]