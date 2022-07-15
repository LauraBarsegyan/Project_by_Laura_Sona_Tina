from fastapi.testclient import TestClient
from app.main import app
import pytest
import requests

client = TestClient(app)


def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello world'
    assert res.status_code == 200


def test_get_one_post_not_exist():
    res =client.get("/115")
    assert res.status_code == 404
