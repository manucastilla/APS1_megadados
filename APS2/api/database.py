import uuid
from typing import Optional, Dict
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

# from api.models import Task

class DBSession:
    tasks = {}
    def __init__(self):
        self.tasks = DBSession.tasks

    def create_tasks_data(self, item):
        uuid_ = uuid.uuid4()
        self.tasks[uuid_] = item
        return uuid_

    def read_tasks_data(self, completed = None):
        if completed is None:
            return self.tasks
        return {
            uuid_: item
            for uuid_, item in self.tasks.items() if item.completed == completed
        }
    def read_task_data(self,uuid_):
        try:
            return self.tasks[uuid_]
        except KeyError as exception:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from exception
    def replace_task_data(self, uuid_,item):   
        try:
            self.tasks[uuid_] = item
        except KeyError as exception:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from exception

    def alter_task_data(self,uuid_,item):
        try:
            update_data = item.dict(exclude_unset=True)
            self.tasks[uuid_] = self.tasks[uuid_].copy(update=update_data)
        except KeyError as exception:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from exception
    def remove_task_data(self,uuid_):
        try:
            del self.tasks[uuid_]
        except KeyError as exception:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from exception    
    

def get_db():
    return DBSession()





