import uuid
from typing import Dict
from fastapi import APIRouter, HTTPException, Depends
from api.models import Task
from api.database import get_db, DBSession

router =APIRouter()

@router.get(
    '',
    tags=['task'],
    summary='Reads task list',
    description='Reads the whole task list.',
    response_model=Dict[uuid.UUID, Task],
)
async def read_tasks(completed: bool = None, db: DBSession = Depends(get_db)):
    if completed is None:
        return db.read_tasks_data()


@router.post(
    '',
    tags=['task'],
    summary='Creates a new task',
    description='Creates a new task and returns its UUID.',
    response_model=uuid.UUID,
)
async def create_task(item: Task,  db: DBSession = Depends(get_db)):
    return db.create_tasks_data(item)

@router.get(
    '/{uuid_}',
    tags=['task'],
    summary='Reads task',
    description='Reads task from UUID.',
    response_model=Task,
)
async def read_task(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        return db.read_task_data(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception


@router.put(
    '/{uuid_}',
    tags=['task'],
    summary='Replaces a task',
    description='Replaces a task identified by its UUID.',
)
async def replace_task(uuid_: uuid.UUID, item: Task,  db: DBSession = Depends(get_db)):
    try:
        db.replace_task_data(uuid_,item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception


@router.patch(
    '/{uuid_}',
    tags=['task'],
    summary='Alters task',
    description='Alters a task identified by its UUID',
)
async def alter_task(uuid_: uuid.UUID, item: Task, db: DBSession = Depends(get_db)):
    try:
        db.alter_task_data(uuid_,item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception


@router.delete(
    '/{uuid_}',
    tags=['task'],
    summary='Deletes task',
    description='Deletes a task identified by its UUID',
)
async def remove_task(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        db.remove_task_data(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception