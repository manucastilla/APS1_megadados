# uvicorn main:app --reload

from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Tasks(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool


tasks_dict ={}

def save_task(task:Tasks):
    task_saved = Tasks(**task.dict())
    return task_saved
    

@app.post("/tasks/", response_model=Tasks)
async def create_task(task: Tasks):
    task_saved = save_task(task)
    tasks_dict[task.title]= task_saved
    return task_saved


@app.get("/tasks/{task_id}", response_model=Tasks, response_model_exclude_unset=True)
async def read_task(tas,task_id: int):
    task_saved = save_task(task)
    return task_saved 


