import pytest
from fastapi import HTTPException, status

from app.auth import get_current_user


@pytest.mark.asyncio
async def test_unauthenticated():
    with pytest.raises(HTTPException) as exception_info:
        await get_current_user(required=True)(token=None)
    assert exception_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert (
        exception_info.value.detail
        == "This endpoint requires authorization. You need to be logged in."
    )
