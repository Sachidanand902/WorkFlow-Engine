from sqlalchemy.orm import Session
from uuid import UUID

from repositories.request_repository import RequestRepository
from domain.entities.request import Request
from domain.entities.approval_action import ApprovalAction
from domain.value_objects.state import RequestState

from infrastructure.persistence.postgres.models import (
    RequestModel,
    ApprovalActionModel,
)


class PostgresRequestRepository(RequestRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, request_id: UUID) -> Request | None:
        model = (
            self._session.query(RequestModel)
            .filter(RequestModel.id == request_id)
            .one_or_none()
        )

        if model is None:
            return None

        approvals = [
            ApprovalAction(
                request_id=a.request_id,
                actor_id=a.actor_id,
                decision=a.decision,
                timestamp=a.timestamp,
                reason=a.reason,
            )
            for a in model.approvals
        ]

        return Request(
            request_id=model.id,
            creator_id=model.creator_id,
            state=RequestState(model.state),
            approvals=approvals,
        )

    def save(self, request: Request) -> None:
        model = (
            self._session.query(RequestModel)
            .filter(RequestModel.id == request.id)
            .one()
        )

        model.state = request.state.value

        existing = {
            (a.actor_id, a.decision)
            for a in model.approvals
        }

        for approval in request.approvals:
            key = (approval.actor_id, approval.decision)
            if key not in existing:
                model.approvals.append(
                    ApprovalActionModel(
                        request_id=approval.request_id,
                        actor_id=approval.actor_id,
                        decision=approval.decision,
                        timestamp=approval.timestamp,
                        reason=approval.reason,
                    )
                )

        self._session.flush()

    def approval_exists(
        self,
        request_id: UUID,
        actor_id: UUID,
        decision: str,
    ) -> bool:
        return (
            self._session.query(ApprovalActionModel)
            .filter_by(
                request_id=request_id,
                actor_id=actor_id,
                decision=decision,
            )
            .count()
            > 0
        )