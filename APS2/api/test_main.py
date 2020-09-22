from fastapi.testclient import TestClient
from .main import app
import uuid

client = TestClient(app)

# ============ POST ============ #
uuids= []
def test_create_task():
    tasks = [
        {
            'description':'teste1',
            'completed':False
        },
        {
            'description':'teste2',
            'completed':True
        },
        {
            'description':'teste3'
        },
        {
            'completed':False
        },
    ]
    
    for task in tasks:
        response = client.post("/task",json=task)
        assert response.status_code == 200
        uuids.append(response.json())

# ============ GET ============ #

def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

def test_read_id_not_found():
    uuid_ = uuid.uuid4()
    response = client.get(f"/task/{uuid_}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_read_list():
    response = client.get("/task")
    assert response.status_code == 200

def test_read_task():
    for tid in uuids:
        response = client.get(f"/task/{tid}")
        assert response.status_code == 200

# ============ PATCH ============ #

def test_change_task_id_not_found():
    uuid_ = uuid.uuid4()
    new_task= {'description':'teste patch', 'completed': True}
    response = client.patch(f"/task/{uuid_}",json=new_task)
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_change_task():
    for tid in uuids:
        new_task= {'description':'teste patch'}
        response = client.patch(f"/task/{tid}", json=new_task)
        assert response.status_code == 200


# ============ PUT ============ #

def change_whole_task_id_not_found():
    uuid_ = uuid.uuid4()
    new_task= {'description':'teste put', 'completed': True}
    response = client.put(f"/task/{uuid_}",json=new_task)
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

# ============ DELETE ============ #

def test_delete_task_id_not_found():
    uuid_ = uuid.uuid4()
    response = client.delete(f"/task/{uuid_}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_task():
    for tid in uuids:
        response = client.delete(f"/task/{tid}")
        assert response.status_code == 200






    



