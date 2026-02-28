from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class ApprovalAction:
    request_id: UUID
    actor_id: UUID
    decision: str  # "APPROVE" or "REJECT"
    timestamp: datetime
    reason: str | None = None