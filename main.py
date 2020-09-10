# uvicorn main:app --reload
from typing import Optional

from fastapi import FastAPI, Path
from pydantic import BaseModel
import uuid
from fastapi.encoders import jsonable_encoder
from uuid import UUID


app = FastAPI(title='Lista de Tarefas',)

# uuid4 funcao para gerar automatico


class Tasks(BaseModel):
    id: UUID = uuid.uuid4()
    title: str
    description: Optional[str] = None
    done: bool


tasks_dict = {}


def save_task(task: Tasks):
    task_saved = Tasks(**task.dict())
    return task_saved


@app.post("/tasks/", response_model=Tasks, tags=[" Cria tarefas"])
async def create_task(task: Tasks):
    task_saved = save_task(task)
    tasks_dict[task.id] = task_saved
    print("KEYYYY:::::")
    print(task.id)
    return task_saved


@app.get("/tasks/{uuid}", response_model=Tasks, response_model_exclude_unset=True, tags=[" Mostra tarefas"])
async def read_task(uuid: str):
    return tasks_dict[uuid]


@app.get("/tasks", tags=[" Mostra tarefas"])
async def read_tasks():
    return tasks_dict


@app.put("/tasks/{uuid}")
async def update_task(uuid: str, task: Tasks):
    # update_item_encoded = tasks_dict[task.id]  # usa json ou não
    update_item_encoded = jsonable_encoder(task)
    tasks_dict[task.id] = update_item_encoded
    return update_item_encoded


@app.patch("/tasks/{uuid}")
async def update_partial_task(uuid: str, task: Tasks):
    stored_item_data = tasks_dict[uuid]
    stored_item_model = Tasks(**stored_item_data)
    update_data = task.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    tasks_dict[uuid] = jsonable_encoder(updated_item)
    return updated_item


# @app.delete("/tasks/{uuid}")
# async def delete_task(uuid: str, task: Tasks):
