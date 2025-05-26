from llama_cpp import Llama
import os

class ModelManager:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.model = None
        self.model_name = None

    def list_models(self):
        return [f for f in os.listdir(self.model_dir) if f.endswith(".gguf")]

    def load_model(self, model_name):
        path = os.path.join(self.model_dir, model_name)
        self.model = Llama(model_path=path, n_ctx=1024, n_threads=4)
        self.model_name = model_name

    def infer(self, prompt):
        if not self.model:
            return "No model loaded."
        result = self.model(prompt, max_tokens=200)
        return result["choices"][0]["text"].strip()
