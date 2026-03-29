from uuid import UUID
from fastapi import Depends, HTTPException, status


class Actor:
    def __init__(self, user_id: UUID):
        self.user_id = user_id


def get_current_actor() -> Actor:
    """
    This will later:
    - Extract JWT from header
    - Validate token
    - Extract user_id
    """
    # Placeholder for now
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication not implemented yet",
    )