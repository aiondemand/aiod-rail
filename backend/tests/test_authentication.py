from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, status

from app.auth import get_current_user_or_raise


@pytest.mark.asyncio
async def test_unauthenticated():
    with pytest.raises(HTTPException) as exception_info:
        await get_current_user_or_raise(token=None)
    assert exception_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert (
        exception_info.value.detail
        == "This endpoint requires authorization. You need to be logged in or provide an API key."
    )


@pytest.mark.asyncio
@patch("app.auth.get_current_user_if_exists", new_callable=AsyncMock)
async def test_get_current_user_returns_userinfo_from_token(mock_verify_token):
    mock_verify_token.return_value = {"email": "john@doe.com", "api_key": "1234"}

    result = await get_current_user_or_raise(token="token")

    mock_verify_token.assert_awaited_once_with("token")
    assert result == mock_verify_token.return_value


@pytest.mark.asyncio
@patch("app.auth.get_current_user_if_exists", new_callable=AsyncMock)
async def test_get_current_user_raises_if_token_not_verified(
    mock_verify_token: AsyncMock,
):
    mock_verify_token.side_effect = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    with pytest.raises(HTTPException) as exception_info:
        await get_current_user_or_raise(token="invalid_token")

    mock_verify_token.assert_awaited_once_with("invalid_token")
    assert exception_info.value.status_code == status.HTTP_401_UNAUTHORIZED
