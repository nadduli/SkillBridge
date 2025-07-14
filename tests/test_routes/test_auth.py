import pytest

user_data={
        "email": "test@example.com",
        "password": "secure123!",
        "full_name": "Test User"}

@pytest.mark.asyncio
async def test_user_registration(async_client):
    response = await async_client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "password" not in response.json()

@pytest.mark.asyncio
async def test_create_user_existing_email(async_client):
    """test register user with existing email"""
    await async_client.post("/api/v1/auth/register", json=user_data)

    response = await async_client.post("/api/v1/auth/register", json=user_data)

    assert response.status_code == 409
    assert response.json()["detail"] == "User with this email already exists."

@pytest.mark.asyncio
def test_user_invalid_email(async_client):
    """test user with invalid email"""
    
