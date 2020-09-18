from fastapi.testclient import TestClient
from main import app
import uuid
#import main

client = TestClient(app)



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
    
# ============ POST ============ #
