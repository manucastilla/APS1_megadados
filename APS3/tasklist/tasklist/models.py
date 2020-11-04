# pylint: disable=missing-module-docstring,missing-class-docstring
from typing import Optional
import uuid
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


# pylint: disable=too-few-public-methods
class Task(BaseModel):
    description: Optional[str] = Field(
        'no description',
        title='Task description',
        max_length=1024,
    )
    completed: Optional[bool] = Field(
        False,
        title='Shows whether the task was completed',
    )
    user_id : uuid.UUID = Field(
        title = 'task_user', 
    )

    class Config:
        schema_extra = {
            'example': {
                'description': 'Buy baby diapers',
                'completed': False,
                'user_id' : '790ac2f1-983b-4a37-87de-26ce642cfaae',
            }
        }

class User(BaseModel):
    name: Optional[str] = Field(
        'no name',
        name='name',
        max_length=1024,
    )
    username: Optional[str] = Field(
        'no username',
        username='username',
        max_length= 1024,
    )

    class Config:
        schema_extra = {
            'example': {
                'name': 'Manuela',
                'username': 'Castilla',
                
            }
        }
