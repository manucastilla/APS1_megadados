# uvicorn main:app --reload
from typing import Optional

from fastapi import FastAPI, Path
from pydantic import BaseModel
import uuid
from uuid import UUID


app = FastAPI(title='Lista de Tarefas',)

## uuid4 funcao para gerar automatico

class Tasks(BaseModel):
    id: UUID = uuid.uuid4()
    title: str
    description: Optional[str] = None
    done: bool


tasks_dict ={}

def save_task(task:Tasks):
    task_saved = Tasks(**task.dict())
    return task_saved
   


@app.post("/tasks/", response_model=Tasks, tags=[" Cria tarefas"])
async def create_task(task: Tasks):
    task_saved = save_task(task)
    tasks_dict[task.id]= task_saved
    print("KEYYYY:::::")
    print( task.id)
    return task_saved
        

@app.get("/tasks/{uuid}", response_model=Tasks, response_model_exclude_unset=True, tags=[" Mostra tarefas"])
async def read_task(uuid :str):
    return tasks_dict[uuid]

@app.get("/tasks",tags=[" Mostra tarefas"])
async def read_tasks():
    return tasks_dict





