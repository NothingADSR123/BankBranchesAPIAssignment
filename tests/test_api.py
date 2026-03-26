from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.database import SessionLocal
from app import models

client = TestClient(app)


def test_banks_returns_200():
    resp = client.get("/banks")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_branch_valid_ifsc_returns_200():
    session = SessionLocal()
    try:
        branch = session.query(models.Branch).first()
        if not branch:
            pytest.skip("No branches in DB to test")
        ifsc = branch.ifsc
    finally:
        session.close()

    resp = client.get("/branches", params={"ifsc": ifsc})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ifsc"] == ifsc
    assert "bank" in data


def test_branch_invalid_ifsc_returns_404():
    resp = client.get("/branches", params={"ifsc": "NOEXIST"})
    assert resp.status_code == 404
