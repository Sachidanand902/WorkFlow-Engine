from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Load a user by ID.
        """
        pass