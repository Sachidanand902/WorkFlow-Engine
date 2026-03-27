from uuid import UUID

from repositories.request_repository import RequestRepository
from domain.errors import DomainError


class RequestLifecycleService:
    def __init__(self, request_repo: RequestRepository):
        self._request_repo = request_repo

    def submit_request(self, request_id: UUID, actor_id: UUID) -> None:
        request = self._request_repo.get_by_id(request_id)

        if request is None:
            raise ValueError("Request not found")

        request.submit(actor_id)

        self._request_repo.save(request)