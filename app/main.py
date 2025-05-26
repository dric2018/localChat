from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.model_manager import ModelManager

app = FastAPI()
manager = ModelManager("app/models")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    with open("app/static/index.html") as f:
        return f.read()

@app.get("/models")
def get_models():
    return manager.list_models()

@app.post("/load")
async def load_model(request: Request):
    data = await request.json()
    manager.load_model(data["model"])
    return {"status": "loaded", "model": data["model"]}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    response = manager.infer(data["prompt"])
    return {"response": response}
