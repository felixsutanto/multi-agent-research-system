# Lightweight setup for HF Spaces
FROM python:3.11-slim

WORKDIR /app

# Minimal system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Copy only what's needed
COPY requirements.txt .
COPY app.py .
COPY src/ ./src/
COPY config/ ./config/

# Install with pip (faster than uv on HF)
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

# Use python directly
CMD ["python", "app.py"]
