from uuid import UUID
from typing import List

from domain.value_objects.state import RequestState
from domain.entities.approval_action import ApprovalAction
from domain.errors import InvalidStateTransition, UnauthorizedAction


class Request:
    def __init__(
        self,
        request_id: UUID,
        creator_id: UUID,
        state: RequestState,
        approvals: List[ApprovalAction] | None = None,
    ):
        self._id = request_id
        self._creator_id = creator_id
        self._state = state
        self._approvals = approvals or []

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def state(self) -> RequestState:
        return self._state

    @property
    def creator_id(self) -> UUID:
        return self._creator_id

    @property
    def approvals(self) -> List[ApprovalAction]:
        return list(self._approvals)

    def submit(self, actor_id: UUID) -> None:
        if actor_id != self._creator_id:
            raise UnauthorizedAction("Only creator can submit the request")

        self._transition_to(RequestState.SUBMITTED)

    def _transition_to(self, next_state: RequestState) -> None:
        if not self._state.can_transition_to(next_state):
            raise InvalidStateTransition(
                f"Cannot transition from {self._state} to {next_state}"
            )

        self._state = next_state

    def record_approval(self, approval: ApprovalAction) -> None:
        if approval.actor_id == self._creator_id:
            raise UnauthorizedAction("Creator cannot approve own request")

        if self._state.is_terminal():
            raise InvalidStateTransition("Cannot approve a terminal request")

        self._approvals.append(approval)