FROM python:3.10

WORKDIR /app

# copy everything
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# install spacy model
RUN python -m spacy download en_core_web_sm

# expose port
EXPOSE 10000

# run app (IMPORTANT FIX HERE)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]