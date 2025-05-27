# Stage 1: Build React frontend
FROM node:18 AS frontend-builder

WORKDIR /app
COPY frontend ./frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# Stage 2: FastAPI app with llama-cpp-python (CPU)
FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    git \
    curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Force CPU build for llama-cpp-python
ENV CMAKE_ARGS="-DLLAMA_CUBLAS=OFF"

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app ./app

# Copy built frontend into app
COPY --from=frontend-builder /app/frontend/dist ./frontend

# Expose port and run API + static UI
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
