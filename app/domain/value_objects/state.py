from enum import Enum


class RequestState(Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

    def is_terminal(self) -> bool:
        return self in {
            RequestState.APPROVED,
            RequestState.REJECTED,
            RequestState.CANCELLED,
        }

    def can_transition_to(self, next_state: "RequestState") -> bool:
        allowed_transitions = {
            RequestState.DRAFT: {RequestState.SUBMITTED},
            RequestState.SUBMITTED: {RequestState.UNDER_REVIEW, RequestState.CANCELLED},
            RequestState.UNDER_REVIEW: {
                RequestState.APPROVED,
                RequestState.REJECTED,
            },
        }

        return next_state in allowed_transitions.get(self, set())