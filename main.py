# uvicorn main:app --reload
from typing import Optional

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel
import uuid
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from enum import Enum


app = FastAPI(title='Lista de Tarefas',)

# uuid4 funcao para gerar automatico


class Tasks(BaseModel):
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
    ''' Esse método cria uma nova tarefa. '''

    tid = uuid.uuid4()
    task_saved = save_task(task)
    tasks_dict[tid] = task_saved
    return task_saved


# @app.get("/listtask/{uuid}", response_model=Tasks, response_model_exclude_unset=True, tags=[" Mostra tarefa especifica"])
# async def read_task(tid: UUID):
#     ''' Esse método  mostra uma tarefa quando um id é especificado. '''
#     return tasks_dict[tid]


@app.get("/listtasks/{tasks_status}",tags=[" Mostra tarefas"])
async def read_tasks(tasks_status: Tasks_Status):
    ''' Esse método lista todas as tarefas, podendo escolher a listagem entre todas as tarefas as tarefas concluidas e as tarefas não concluidas'''
    listagem={}
    print(tasks_status)
    if tasks_status == Tasks_Status.concluida:
        for t in tasks_dict:
            if tasks_dict[t].done == True:
                listagem[t]=tasks_dict[t]
        return listagem

    elif tasks_status == Tasks_Status.naoconcluida:
        for t in tasks_dict:
            print(tasks_dict[t])
            if tasks_dict[t].done == False:
                listagem[t]=tasks_dict[t]
        return listagem

    elif tasks_status == Tasks_Status.todas:
        return tasks_dict




@app.patch("/changetaskdescription/{uuid}",tags=[" Altera descrição da tarefa"])
async def update_task_description(tid: UUID,newvalue: str):
    ''' Esse método altera a descrição de uma tarefa. '''
    # stored_item_data = tasks_dict[tid]
    # stored_item_model = Tasks(**stored_item_data)
    # update_data = task.dict(exclude_unset=True)
    # updated_item = tasks_dict[tid].copy(update=update_data)
    # tasks_dict[tid] = jsonable_encoder(updated_item)
    tasks_dict[tid].description =newvalue
    return tasks_dict[tid]

@app.patch("/changetaskdone/{uuid}",tags=[" Altera status da tarefa"])
async def update_task_done(tid: UUID, newvalue: bool):
    ''' Esse método altera o status de uma tarefa, se está concluida ou não. '''
    tasks_dict[tid].done =newvalue
    return tasks_dict[tid]

@app.put("/updatetasks/{uuid}",response_model=Tasks, response_model_exclude_unset=True, tags=[" Altera tarefa inteira"])
async def update_task(tid: UUID, task: Tasks):
    ''' Esse método altera uma tarefa pro completo. '''
    # update_item_encoded = tasks_dict[task.id]  # usa json ou não
    update_item_encoded = jsonable_encoder(task)
    tasks_dict[tid] = update_item_encoded
    return update_item_encoded


@app.delete("/deltasks/{uuid}", tags=[" Apaga tarefa "])
async def delete_task(tid: UUID):
    ''' Esse método apaga uma tarefa do nosso banco de dados. '''
    tasks_dict.pop(tid,None)
    return tasks_dict


