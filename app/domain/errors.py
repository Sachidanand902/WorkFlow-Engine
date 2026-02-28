class DomainError(Exception):
    """Base class for all domain errors."""
    pass


class InvalidStateTransition(DomainError):
    pass


class UnauthorizedAction(DomainError):
    pass


class DuplicateApproval(DomainError):
    pass