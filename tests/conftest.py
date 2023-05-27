"""Test configuration file."""
import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.app import app
from app.config import DATABASE_URL_TEST
from app.db import Base, get_db

engine = create_engine(DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=True, bind=engine,
)


def override_get_db():
    """Override get_db function."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db_engine():
    """Create database engine."""
    engine_test = create_engine(DATABASE_URL_TEST)
    yield engine_test
    engine_test.dispose()


@pytest.fixture(scope="function")
def test_session(db_engine, apply_migrations):
    """Create database session."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="session")
def alembic_config(db_engine):
    """Create alembic config."""
    test_config = Config()
    test_config.set_main_option("script_location", "migrations/")
    test_config.set_main_option("sqlalchemy.url", DATABASE_URL_TEST)
    test_config.attributes["connection"] = db_engine.connect()
    yield test_config
    test_config.attributes["connection"].close()


@pytest.fixture(scope="session")
def apply_migrations(alembic_config):
    """Apply migrations."""
    command.upgrade(alembic_config, "head")


@pytest.fixture(scope="session")
def test_client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def drop_tables(request, db_engine):
    """Drop all tables after test session."""
    def teardown():
        with db_engine.begin() as connection:
            Base.metadata.drop_all(bind=connection)
            connection.execute(text("DROP TABLE IF EXISTS alembic_version"))

    request.addfinalizer(teardown)
    yield None
