sudo docker build -t gpt4local-full .
sudo docker run -p 8000:8000 -v $(pwd)/app/models:/app/app/models gpt4local-full