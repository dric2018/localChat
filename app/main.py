from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os, shutil
from .model_manager import ModelManager

app = FastAPI()
manager = ModelManager("app/models")
chat_history = []

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.get("/api/models")  # <-- must include /api
def get_models():
    return manager.list_models()

@app.post("/api/load")
async def load_model(request: Request):
    data = await request.json()
    manager.load_model(data["model"])
    return {"status": "loaded", "model": data["model"]}

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data["prompt"]
    full_prompt = "\n".join([f"User: {h['q']}\nAI: {h['a']}" for h in chat_history]) + f"\nUser: {prompt}\nAI:"
    response = manager.infer(full_prompt)
    chat_history.append({"q": prompt, "a": response})
    return {"response": response, "history": chat_history}

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    path = os.path.join("app/uploads", file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"status": "uploaded", "filename": file.filename}
