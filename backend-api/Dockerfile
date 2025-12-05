FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port
EXPOSE $PORT

# Start the application
CMD uvicorn api.main:app --host 0.0.0.0 --port $PORT
