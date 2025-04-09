"""Integration tests for QR Code API."""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_login_for_access_token():
    """Test successful login returns access token."""
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/token", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_create_qr_code_unauthorized():
    """Test unauthorized QR code creation fails."""
    qr_request = {
        "url": "https://example.com",
        "fill_color": "red",
        "back_color": "white",
        "size": 10,
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/qr-codes/", json=qr_request)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_and_delete_qr_code():
    """Test QR code creation and deletion with valid auth."""
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        token_response = await ac.post("/token", data=form_data)
        access_token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        qr_request = {
            "url": "https://example.com",
            "fill_color": "red",
            "back_color": "white",
            "size": 10,
        }
        create_response = await ac.post("/qr-codes/", json=qr_request, headers=headers)
        assert create_response.status_code in [201, 409]

        if create_response.status_code == 201:
            qr_code_url = create_response.json()["qr_code_url"]
            qr_filename = qr_code_url.split('/')[-1]
            delete_response = await ac.delete(f"/qr-codes/{qr_filename}", headers=headers)
            assert delete_response.status_code == 204
