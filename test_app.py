import pytest
from app import app, db, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()

def test_add_task(client):
    response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'Test Description'
    })
    assert response.status_code == 201
    assert b'Task created' in response.data

def test_get_tasks(client):
    # Add a task first
    client.post('/tasks', json={'title': 'Task 1'})
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Task 1'

def test_update_task(client):
    client.post('/tasks', json={'title': 'Task to update'})
    response = client.put('/tasks/1', json={'completed': True})
    assert response.status_code == 200
    assert b'Task updated' in response.data

def test_delete_task(client):
    client.post('/tasks', json={'title': 'Task to delete'})
    response = client.delete('/tasks/1')
    assert response.status_code == 200
    assert b'Task deleted' in response.data
