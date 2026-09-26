from fastapi import Depends, HTTPException, status

from app.auth.dependency import get_current_user
from app.core.enums import UserRole
from app.models.user import User


def require_reviewer(
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.PROVIDER,
    }:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to review claims",
        )

    return current_user