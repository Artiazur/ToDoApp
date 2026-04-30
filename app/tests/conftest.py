from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from app.core.database import get_db, create_engine, sessionmaker, Base
from app.main import app
from pytest import fixture


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@fixture(scope="function")
def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@fixture(scope="module", autouse=True)
def override_dependencies(override_get_db):
    app.dependency_overrides[get_db] = lambda: override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)


@fixture(scope="session", autouse=True)
def create_and_drop_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@fixture(scope="function")
def create_client():
    client = TestClient(app)
    yield client
