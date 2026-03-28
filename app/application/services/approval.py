from datetime import datetime
from uuid import UUID

from repositories.request_repository import RequestRepository
from domain.entities.approval_action import ApprovalAction
from domain.errors import DuplicateApproval


class ApprovalService:
    def __init__(self, request_repo: RequestRepository):
        self._request_repo = request_repo

    def attempt_approval(
        self,
        request_id: UUID,
        actor_id: UUID,
        decision: str,
        reason: str | None = None,
    ) -> None:
        request = self._request_repo.get_by_id(request_id)

        if request is None:
            raise ValueError("Request not found")

        if self._request_repo.approval_exists(
            request_id=request_id,
            actor_id=actor_id,
            decision=decision,
        ):
            raise DuplicateApproval("Approval already exists")

        approval = ApprovalAction(
            request_id=request_id,
            actor_id=actor_id,
            decision=decision,
            timestamp=datetime.utcnow(),
            reason=reason,
        )

        request.record_approval(approval)
        
        self._request_repo.save(request)