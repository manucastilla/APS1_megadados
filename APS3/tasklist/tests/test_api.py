# pylint: disable=missing-module-docstring,missing-function-docstring
import os.path

from fastapi.testclient import TestClient

from utils import utils

from tasklist.main import app

client = TestClient(app)

app.dependency_overrides[utils.get_config_filename] = \
    utils.get_config_test_filename


def setup_database():
    scripts_dir = os.path.join(
        os.path.dirname(__file__),
        '..',
        'database',
        'migrations',
    )
    config_file_name = utils.get_config_test_filename()
    secrets_file_name = utils.get_admin_secrets_filename()
    utils.run_all_scripts(scripts_dir, config_file_name, secrets_file_name)


def test_read_main_returns_not_found():
    setup_database()
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

#######################################
def test_create_and_read_some_users():
    setup_database()
    users = [
        {
            "name": "manuela",
            "username": "castilla",
        },
        {
            "name": "maria eduarda",
            "username": "bicalho",
        },
        {
            "name": "matheus",
        },
        {
            "username": "ramos",
        },
        {},
    ]
    expected_responses = [
        {
            'name': 'manuela',
            'username': 'castilla',
        },
        {
            'name': 'maria eduarda',
            'username': 'bicalho',
        },
        {
            'name': 'matheus',
            'username': 'no username',
        },
        {
           'name': 'no name',
            'username': 'ramos',
        },
        {
            'name': 'no name',
            'username': 'no username',
        },
    ]

    # Insert some users and check that all succeeded.
    uuids = []
    for user in users:
        response = client.post("/user", json=user)
        assert response.status_code == 200
        uuids.append(response.json())

    #Read the complete list of tasks.
    def get_expected_responses_with_uuid():
        return {uuid_: response for uuid_, response in zip(uuids, expected_responses)}

    response = client.get('/user')
    assert response.status_code == 200
    assert response.json() == get_expected_responses_with_uuid()

    # # Read only completed tasks.
    # for completed in [False, True]:
    #     response = client.get(f'/task?completed={str(completed)}')
    #     assert response.status_code == 200
    #     assert response.json() == get_expected_responses_with_uuid(completed)

    # Delete all users.
    for uuid_ in uuids:
        response = client.delete(f'/user/{uuid_}')
        assert response.status_code == 200

    # Check whether there are no more users.
    response = client.get('/user')
    assert response.status_code == 200
    assert response.json() == {}


def test_read_users_with_no_user():
    setup_database()
    response = client.get("/user")
    assert response.status_code == 200
    assert response.json() == {}

def test_substitute_user():
    setup_database()

    user = {
        'name' : 'Lucas',
        'username' : 'Muchaluat',
    }

    response = client.post("/user", json=user)
    assert response.status_code == 200
    uuid_ = response.json()


    # Replace the task.
    new_user = {'name': 'Lulu', 'username': "Muchu"}
    response = client.put(f'/user/{uuid_}', json=new_user)
    assert response.status_code == 200

    # Check whether the task was replaced.
    response = client.get(f'/user/{uuid_}')
    assert response.status_code == 200
    assert response.json() == new_user

    # Delete the task.
    response = client.delete(f'/user/{uuid_}')
    assert response.status_code == 200

    # Delete the task.
    response = client.delete(f'/user')
    assert response.status_code == 200


def test_alter_user():
    setup_database()

    user = {
        'name' : 'Luciana',
        'username' : 'castilla',
    }

    response = client.post("/user", json=user)
    assert response.status_code == 200
    uuid_ = response.json()

    # Replace the task.
    new_user_partial = {'name': 'Juan', "username": "Carlos",}
    response = client.patch(f'/user/{uuid_}', json=new_user_partial)
    assert response.status_code == 200

    # Check whether the task was altered.
    response = client.get(f'/user/{uuid_}')
    assert response.status_code == 200
    assert response.json() == {**user, **new_user_partial}

    # Delete the task.
    response = client.delete(f'/user/{uuid_}')
    assert response.status_code == 200


def test_read_invalid_user():
    setup_database()

    response = client.get('/user/invalid_uuid')
    assert response.status_code == 422


def test_read_nonexistant_user():
    setup_database()

    response = client.get('/user/3668e9c9-df18-4ce2-9bb2-82f907cf110c')
    assert response.status_code == 404


def test_delete_invalid_user():
    setup_database()

    response = client.delete('/user/invalid_uuid')
    assert response.status_code == 422


def test_delete_nonexistant_user():
    setup_database()

    response = client.delete('/user/3668e9c9-df18-4ce2-9bb2-82f907cf110c')
    assert response.status_code == 404


def test_delete_all_users():
    setup_database()

    user = {
        'name' : 'Bonnie',
        'username' : 'Muchaluat',
    }

    response = client.post("/user", json=user)
    assert response.status_code == 200
    uuid_ = response.json()

    # Check whether the task was inserted.
    response = client.get('/user')
    assert response.status_code == 200
    assert response.json() == {uuid_: user}

    # Delete all tasks.
    response = client.delete('/user')
    assert response.status_code == 200

    # Check whether all tasks have been removed.
    response = client.get('/user')
    assert response.status_code == 200
    assert response.json() == {}


#######################################

def test_read_tasks_with_no_task():
    setup_database()
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json() == {}



def test_create_and_read_some_tasks():
    setup_database()

    user = {
        'name' : 'duda',
        'username' : 'castilla',
    }

    response = client.post("/user", json=user)
    assert response.status_code == 200
    user_id = response.json()

    tasks = [
        {
            "description": "foo",
            "completed": False,
            "user_id" : user_id,
        },
        {
            "description": "bar",
            "completed": True,
            "user_id" : user_id ,
        },
        {
            "description": "baz",
            "user_id" : user_id ,
        },
        {
            "completed": True,
            "user_id" : user_id ,
        },
        {
            "user_id" : user_id ,
        },
    ]
    expected_responses = [
        {
            'description': 'foo',
            'completed': False,
            "user_id" : user_id ,
        },
        {
            'description': 'bar',
            'completed': True,
            "user_id" : user_id ,
        },
        {
            'description': 'baz',
            'completed': False,
            "user_id" : user_id ,
        },
        {
            'description': 'no description',
            'completed': True,
            "user_id" : user_id ,
        },
        {
            'description': 'no description',
            'completed': False,
            "user_id" : user_id ,
        },
    ]

    # Insert some tasks and check that all succeeded.
    uuids = []
    for task in tasks:
        response = client.post("/task", json=task)
        assert response.status_code == 200
        uuids.append(response.json())

    # Read the complete list of tasks.
    def get_expected_responses_with_uuid(completed=None):
        return {
            uuid_: response
            for uuid_, response in zip(uuids, expected_responses)
            if completed is None or response['completed'] == completed
        }

    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == get_expected_responses_with_uuid()

    # Read only completed tasks.
    for completed in [False, True]:
        response = client.get(f"/task?completed={str(completed)}")
        assert response.status_code == 200
        assert response.json() == get_expected_responses_with_uuid(completed)

    # Delete all tasks.
    for uuid_ in uuids:
        response = client.delete(f'/task/{uuid_}')
        assert response.status_code == 200

    # Check whether there are no more tasks.
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}

    # Delete all users.
    response = client.delete("/user")
    assert response.status_code == 200


def test_substitute_task():
    setup_database()

    user = {
        'name' : 'duda',
        'username' : 'castilla',
    }

    response = client.post("/user", json=user)
    assert response.status_code == 200
    user_id = response.json()

    # Create a task.
    task = {
        'description': 'foo', 
        'completed': False,
        "user_id" : user_id,
        }
    response = client.post('/task', json=task)
    assert response.status_code == 200
    uuid_ = response.json()

    # Replace the task.
    new_task = {'description': 'bar', 'completed': True, "user_id" : user_id,}
    response = client.put(f'/task/{uuid_}', json=new_task)
    assert response.status_code == 200

    # Check whether the task was replaced.
    response = client.get(f'/task/{uuid_}')
    assert response.status_code == 200
    assert response.json() == new_task

    # Delete the task.
    response = client.delete(f'/task/{uuid_}')
    assert response.status_code == 200

    # Delete the task.
    response = client.delete(f'/user')
    assert response.status_code == 200


def test_alter_task():
    setup_database()

    user = {
        'name' : 'duda',
        'username' : 'castilla',
    }

    response = client.post("/user", json=user)
    assert response.status_code == 200
    user_id = response.json()


    # Create a task.
    task = {'description': 'foo', 'completed': False, "user_id": user_id,}
    response = client.post('/task', json=task)
    assert response.status_code == 200
    uuid_ = response.json()

    # Replace the task.
    new_task_partial = {'completed': True, "user_id": user_id,}
    response = client.patch(f'/task/{uuid_}', json=new_task_partial)
    assert response.status_code == 200

    # Check whether the task was altered.
    response = client.get(f'/task/{uuid_}')
    assert response.status_code == 200
    assert response.json() == {**task, **new_task_partial}

    # Delete the task.
    response = client.delete(f'/task/{uuid_}')
    assert response.status_code == 200


def test_read_invalid_task():
    setup_database()

    response = client.get('/task/invalid_uuid')
    assert response.status_code == 422


def test_read_nonexistant_task():
    setup_database()

    response = client.get('/task/3668e9c9-df18-4ce2-9bb2-82f907cf110c')
    assert response.status_code == 404


def test_delete_invalid_task():
    setup_database()

    response = client.delete('/task/invalid_uuid')
    assert response.status_code == 422


def test_delete_nonexistant_task():
    setup_database()

    response = client.delete('/task/3668e9c9-df18-4ce2-9bb2-82f907cf110c')
    assert response.status_code == 404


def test_delete_all_tasks():
    setup_database()

    user = {
        'name' : 'duda',
        'username' : 'castilla',
    }

    response = client.post("/user", json=user)
    assert response.status_code == 200
    user_id = response.json()

    # Create a task.
    task = {'description': 'foo', 'completed': False, "user_id": user_id,}
    response = client.post('/task', json=task)
    assert response.status_code == 200
    uuid_ = response.json()

    # Check whether the task was inserted.
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {uuid_: task}

    # Delete all tasks.
    response = client.delete('/task')
    assert response.status_code == 200

    # Check whether all tasks have been removed.
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}
