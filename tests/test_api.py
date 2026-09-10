import os
os.environ['DATABASE_URL']='sqlite:///./test_sign_language.db'
import pytest
from fastapi.testclient import TestClient
from backend.app import app
@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client
def test_health(client):
    response=client.get('/api/health')
    assert response.status_code==200
    assert response.json()['status']=='ok'
    assert response.json()['database_available'] is True
def test_authentication(client):
    email='test-person@example.com'
    response=client.post('/api/auth/signup',json={'email':email,'password':'safe-password-8'})
    assert response.status_code in (201,409)
    response=client.post('/api/auth/login',json={'email':email,'password':'safe-password-8'})
    assert response.status_code==200
    assert response.json()['token_type']=='bearer'
