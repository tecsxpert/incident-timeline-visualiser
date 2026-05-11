FROM python:3.11-slim

WORKDIR /app

# Install build tools needed by chromadb/hnswlib (removed after install to keep image small)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# gunicorn handles multiple requests — safer for demo
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]