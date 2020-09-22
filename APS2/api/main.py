# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring


# pylint: disable=too-few-public-methods
# class Task(BaseModel):
#     description: Optional[str] = Field(
#         'no description',
#         title='Task description',
#         max_length=1024,
#     )
#     completed: Optional[bool] = Field(
#         False,
#         title='Shows whether the task was completed',
#     )

#     class Config:
#         schema_extra = {
#             'example': {
#                 'description': 'Buy baby diapers',
#                 'completed': False,
#             }
#         }

# class DBSession:
#     tasks = {}
#     def __init__(self):
#         self.tasks = DBSession.tasks

# def get_db():
#     return DBSession()
# tasks = {}





from fastapi import FastAPI, HTTPException, APIRouter

from api.routers import task

tags_metadata = [
    {
        'name': 'task',
        'description': 'Operations related to tasks.',
    },
]

app = FastAPI(
    title='Task list',
    description='Task-list project for the **Megadados** course',
    openapi_tags=tags_metadata,
)

app.include_router(task.router, prefix='/task',tags=['task'])



