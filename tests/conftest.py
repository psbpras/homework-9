"""Fixtures for QR Code API tests."""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def async_client():
    """Provides an AsyncClient instance for testing."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture
async def get_access_token_for_test(async_client):
    """Logs in as admin and returns an access token."""
    form_data = {"username": "admin", "password": "secret"}
    response = await async_client.post("/token", data=form_data)
    return response.json()["access_token"]
