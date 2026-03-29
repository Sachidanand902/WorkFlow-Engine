from repositories.request_repository import RequestRepository
from application.services.request_lifecycle import RequestLifecycleService
from application.services.approval import ApprovalService


def get_request_lifecycle_service(
    request_repo: RequestRepository,
) -> RequestLifecycleService:
    return RequestLifecycleService(request_repo)


def get_approval_service(
    request_repo: RequestRepository,
) -> ApprovalService:
    return ApprovalService(request_repo)