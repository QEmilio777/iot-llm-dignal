from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.llm_adapter import LLMAdapter
from app.actions import ActionService

app = FastAPI()

# Archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Instancias
llm = LLMAdapter()
actions = ActionService()


# Modelo de entrada
class PromptRequest(BaseModel):
    prompt: str


# Ruta principal (carga el HTML)
@app.get("/")
def home():
    return FileResponse("static/index.html")


# Endpoint para procesar prompts
@app.post("/api/prompt")
def process_prompt(data: PromptRequest):
    try:
        llm_output = llm.ask(data.prompt)
        final_answer = actions.execute(llm_output)

        return {
            "prompt": data.prompt,
            "llm_output": llm_output,
            "answer": final_answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))