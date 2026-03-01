from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from domain.entities.request import Request
from domain.entities.approval_action import ApprovalAction


class RequestRepository(ABC):

    @abstractmethod
    def get_by_id(self, request_id: UUID) -> Optional[Request]:
        """
        Load a full Request aggregate by ID.
        Returns None if the request does not exist.
        """
        pass

    @abstractmethod
    def save(self, request: Request) -> None:
        """
        Persist the entire Request aggregate atomically.
        Must detect concurrent modification.
        """
        pass

    @abstractmethod
    def approval_exists(
        self,
        request_id: UUID,
        actor_id: UUID,
        decision: str,
    ) -> bool:
        """
        Check whether an approval action already exists
        for idempotency purposes.
        """
        pass