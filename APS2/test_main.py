from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

class DBSession:
    tasks = {}
    def __init__(self):
        self.tasks = DBSession.tasks
    def get_db():
        return DBSession()

def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}