# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Expose port (Railway will override this with $PORT)
EXPOSE 8000

# Start command - Railway will set $PORT automatically
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
