FROM python:3.10-slim

WORKDIR /app/backend

COPY requirements.txt ../requirements.txt
COPY backend/ .

RUN pip install --no-cache-dir -r ../requirements.txt
RUN python -m spacy download en_core_web_sm

EXPOSE 10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]