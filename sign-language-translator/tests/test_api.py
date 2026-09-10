import os
os.environ['DATABASE_URL']='sqlite:///./test_sign_language.db'
from fastapi.testclient import TestClient
from backend.app import app
client=TestClient(app)
def test_health():
 r=client.get('/api/health');assert r.status_code==200 and r.json()['status']=='ok'
def test_authentication():
 email='test-person@example.com';r=client.post('/api/auth/signup',json={'email':email,'password':'safe-password-8'});assert r.status_code in (201,409)
 r=client.post('/api/auth/login',json={'email':email,'password':'safe-password-8'});assert r.status_code==200
