import pytest

from app import app

@pytest.fixture
def test_index(app, client):
    res = client.get("/")
    assert res.status == 200