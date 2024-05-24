from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException, status

from app.authentication import get_current_user


@pytest.mark.asyncio
async def test_unauthenticated():
    with pytest.raises(HTTPException) as exception_info:
        await get_current_user(required=True)(token=None)
    assert exception_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert (
        exception_info.value.detail
        == "This endpoint requires authorization. You need to be logged in or provide an API key."
    )


@pytest.mark.asyncio
async def test_current_get_user_from_token_or_from_api_key_must_be_true():
    with pytest.raises(ValueError) as exception_info:
        await get_current_user(required=True, from_token=False, from_api_key=False)(
            token="token"
        )
    assert (
        str(exception_info.value)
        == "Either from_token or from_api_key must be set to True"
    )


@pytest.mark.asyncio
@patch("app.authentication._verify_token", new_callable=AsyncMock)
async def test_get_current_user_returns_userinfo_from_token(mock_verify_token):
    mock_verify_token.return_value = {"email": "john@doe.com", "api_key": "1234"}

    result = await get_current_user(required=True, from_token=True, from_api_key=False)(
        token="token"
    )

    mock_verify_token.assert_awaited_once_with("token")
    assert result == mock_verify_token.return_value


@pytest.mark.asyncio
@patch("app.authentication._verify_token", new_callable=AsyncMock)
async def test_get_current_user_raises_if_token_not_verified(
    mock_verify_token: AsyncMock,
):
    mock_verify_token.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
    )

    with pytest.raises(HTTPException) as exception_info:
        await get_current_user(required=True, from_token=True, from_api_key=False)(
            token="invalid_token"
        )

    mock_verify_token.assert_awaited_once_with("invalid_token")
    assert exception_info.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
@patch("app.models.user.User.find_one", new_callable=AsyncMock)
async def test_get_current_user_returns_user_from_api_key(mock_find_one: AsyncMock):
    mock_user = Mock()
    mock_user.to_dict.return_value = {"email": "john@doe.com", "api_key": "1234"}
    mock_find_one.return_value = mock_user

    user = await get_current_user(required=True, from_token=False, from_api_key=True)(
        api_key="1234"
    )

    assert user == mock_user.to_dict.return_value
    mock_find_one.assert_awaited_once_with({"api_key": "1234"})


@pytest.mark.asyncio
@patch("app.models.user.User.find_one", new_callable=AsyncMock)
async def test_get_current_user_raises_if_api_key_invalid(mock_find_one: AsyncMock):
    mock_find_one.return_value = None

    with pytest.raises(HTTPException) as exception_info:
        await get_current_user(required=True, from_token=False, from_api_key=True)(
            api_key="invalid_api_key"
        )

    assert exception_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    mock_find_one.assert_awaited_once_with({"api_key": "invalid_api_key"})
