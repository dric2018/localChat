#!/bin/bash

set -e  # Stop on error

echo "👉 Building Docker image..."
sudo docker build -t gpt4local-full .

echo "👉 Running Docker container..."
sudo docker run -p 8000:8000 -v $(pwd)/app/models:/app/app/models gpt4local-full