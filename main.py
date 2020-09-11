# uvicorn main:app --reload
from typing import Optional

from fastapi import FastAPI, Path
from pydantic import BaseModel
import uuid
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from enum import Enum


app = FastAPI(title='Lista de Tarefas',)

# uuid4 funcao para gerar automatico



class Tasks(BaseModel):
    id: UUID = None
    title: str
    description: Optional[str] = None
    done: bool

class Tasks_Status(str, Enum):
    concluida = "concluida"
    naoconcluida = "naoconcluida"
    todas="todas"


tasks_dict = {}


def save_task(task: Tasks):
    task_saved = Tasks(**task.dict())
    return task_saved


@app.post("/tasks/", response_model=Tasks, tags=[" Cria tarefas"])
async def create_task(task: Tasks):
    ''' Esse método cria uma nova tarefa. Não são necessários parâmetros para chamar esse método.'''

    task.id = uuid.uuid4()
    task_saved = save_task(task)
    tasks_dict[task.id] = task_saved
    return task_saved


@app.get("/listTask/{uuid}", response_model=Tasks, response_model_exclude_unset=True, tags=[" Mostra tarefa especifica"])
async def read_task(uuid: UUID):
    return tasks_dict[uuid]


@app.get("/listTasks/{tasks_status}",response_model=dict, response_model_exclude_unset=True,tags=[" Mostra tarefas"])
async def read_tasks(tasks_status: Tasks_Status):
    ''' Lista todas as tarefas '''
    listagem={}
    print(tasks_status)
    if tasks_status == Tasks_Status.concluida:
        for t in tasks_dict:
            if tasks_dict[t].done == True:
                listagem[tasks_dict[t].id]=tasks_dict[t]
        return listagem

    elif tasks_status == Tasks_Status.naoconcluida:
        for t in tasks_dict:
            print(tasks_dict[t])
            if tasks_dict[t].done == False:
                listagem[tasks_dict[t].id]=tasks_dict[t]
        return listagem

    elif tasks_status == Tasks_Status.todas:
        return tasks_dict



@app.put("/updateTasks/{uuid}",response_model=Tasks, response_model_exclude_unset=True, tags=[" Altera tarefa "])
async def update_task(uuid: UUID, task: Tasks):
    # update_item_encoded = tasks_dict[task.id]  # usa json ou não
    update_item_encoded = jsonable_encoder(task)
    tasks_dict[task.id] = update_item_encoded
    return update_item_encoded


@app.patch("/changeTasks/{uuid}",tags=[" Altera caracteritica da tarefa "])
async def update_partial_task(uuid: UUID, task: Tasks):
    stored_item_data = tasks_dict[uuid]
    stored_item_model = Tasks(**stored_item_data)
    update_data = task.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    tasks_dict[uuid] = jsonable_encoder(updated_item)
    return updated_item






@app.delete("/delTasks/{uuid}",response_model=Tasks, response_model_exclude_unset=True, tags=[" Apaga tarefa "])
async def delete_task(uuid: UUID, task: Tasks):
    print(uuid)
    tasks_dict.pop(uuid,None)
    return tasks_dict


