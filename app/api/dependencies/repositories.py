from sqlalchemy.orm import Session

from infrastructure.persistence.postgres.request_repo import PostgresRequestRepository
from repositories.request_repository import RequestRepository


def get_request_repository(db: Session) -> RequestRepository:
    return PostgresRequestRepository(db)