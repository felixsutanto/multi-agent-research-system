# Multi-Agent Research System
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY src/ ./src/
COPY config/ ./config/
COPY app.py .

# Install dependencies
RUN uv sync --no-dev

# Expose port 7860 (Hugging Face Spaces requirement)
EXPOSE 7860

# Run the Gradio app
CMD ["uv", "run", "python", "app.py"]
