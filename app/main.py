from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import UploadFile, File
import shutil

from app.model_manager import ModelManager

app = FastAPI()
manager = ModelManager("app/models")

# Serve React build from /frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.get("/api/models")
def get_models():
    return manager.list_models()

@app.post("/api/load")
async def load_model(request: Request):
    data = await request.json()
    manager.load_model(data["model"])
    return {"status": "loaded", "model": data["model"]}

chat_history = []

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data["prompt"]
    full_prompt = "\n".join([f"User: {p['q']}\nAI: {p['a']}" for p in chat_history]) + f"\nUser: {prompt}\nAI:"

    response = manager.infer(full_prompt)
    chat_history.append({"q": prompt, "a": response})
    return {"response": response, "history": chat_history}

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    path = f"app/uploads/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "uploaded", "filename": file.filename}

