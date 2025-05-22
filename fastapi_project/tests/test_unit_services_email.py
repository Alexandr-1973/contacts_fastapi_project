import pytest
from unittest.mock import AsyncMock, patch
from fastapi_mail.errors import ConnectionErrors
from fastapi_project.src.services.email import send_email, send_rp_email


@pytest.mark.asyncio
@patch("fastapi_project.src.services.email.FastMail")
@patch("fastapi_project.src.services.email.auth_service.create_email_token", return_value="fake_token")
async def test_send_email_success(mock_create_token, mock_fastmail):
    mock_fm_instance = AsyncMock()
    mock_fastmail.return_value = mock_fm_instance

    await send_email(
        email="test@example.com",
        username="testuser",
        host="http://localhost:8000"
    )

    mock_create_token.assert_called_once_with({"sub": "test@example.com"})
    mock_fm_instance.send_message.assert_awaited_once()
    args, kwargs = mock_fm_instance.send_message.call_args
    assert kwargs["template_name"] == "email_template.html"


@pytest.mark.asyncio
@patch("fastapi_project.src.services.email.FastMail")
@patch("fastapi_project.src.services.email.auth_service.create_email_token", return_value="fake_token")
async def test_send_rp_email_success(mock_create_token, mock_fastmail):
    mock_fm_instance = AsyncMock()
    mock_fastmail.return_value = mock_fm_instance
    await send_rp_email(
        email="test@example.com",
        username="testuser",
        host="http://localhost:8000"
    )

    mock_create_token.assert_called_once_with({"sub": "test@example.com"})
    mock_fm_instance.send_message.assert_awaited_once()
    args, kwargs = mock_fm_instance.send_message.call_args
    assert kwargs["template_name"] == "email_rp_template.html"


@pytest.mark.asyncio
@patch("fastapi_project.src.services.email.FastMail.send_message", new_callable=AsyncMock)
@patch("fastapi_project.src.services.email.auth_service.create_email_token", return_value="fake_token")
async def test_send_email_connection_error(mock_create_token, mock_send_message):
    mock_send_message.side_effect = ConnectionErrors("Connection failed")

    await send_email(
        email="test@example.com",
        username="testuser",
        host="http://localhost:8000"
    )

    mock_create_token.assert_called_once()
    mock_send_message.assert_awaited_once()


@pytest.mark.asyncio
@patch("fastapi_project.src.services.email.FastMail.send_message", new_callable=AsyncMock)
@patch("fastapi_project.src.services.email.auth_service.create_email_token", return_value="fake_token")
async def test_send_rp_email_connection_error(mock_create_token, mock_send_message):
    mock_send_message.side_effect = ConnectionErrors("Connection failed - Test - OK")

    await send_rp_email(
        email="test@example.com",
        username="testuser",
        host="http://localhost:8000"
    )

    mock_create_token.assert_called_once()
    mock_send_message.assert_awaited_once()
