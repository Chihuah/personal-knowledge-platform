from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db_session
from app.dependencies import get_task_dispatcher
from app.main import app
from app.tasks.dispatcher import DispatchResult


class FakeDispatcher:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def enqueue_ingestion(self, item_id) -> DispatchResult:
        self.calls.append(str(item_id))
        return DispatchResult(attempted=True, message="Queued in test dispatcher.")


@pytest.fixture
def testing_session_factory():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    Base.metadata.create_all(engine)
    try:
        yield TestingSessionLocal
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def db_session(testing_session_factory) -> Generator[Session, None, None]:
    session = testing_session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def dispatcher() -> FakeDispatcher:
    return FakeDispatcher()


@pytest.fixture
def client(
    db_session: Session,
    dispatcher: FakeDispatcher,
) -> Generator[TestClient, None, None]:
    def override_db_session() -> Generator[Session, None, None]:
        yield db_session

    def override_task_dispatcher() -> FakeDispatcher:
        return dispatcher

    app.dependency_overrides[get_db_session] = override_db_session
    app.dependency_overrides[get_task_dispatcher] = override_task_dispatcher
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
