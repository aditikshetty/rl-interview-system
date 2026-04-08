FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for better caching
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . /app

# Environment Variables
ENV MODEL_NAME="openai/gpt-oss-20b"
ENV API_BASE_URL="https://router.huggingface.co"

# Expose port (HF Spaces defaults to 7860)
EXPOSE 7860

# Start FastAPI server via uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
