import pytest
from unittest.mock import Mock, patch
import database
import oracledb

@pytest.fixture(autouse=True)
def mocked_env(monkeypatch):
    monkeypatch.setenv("DATABASE_USER", "test")
    monkeypatch.setenv("DATABASE_PASSWORD", "test")
    monkeypatch.setenv("DATABASE_HOST", "test_host")
    monkeypatch.setenv("DATABASE_PORT", "1521")
    monkeypatch.setenv("DATABASE_SID", "test_sid")
    monkeypatch.setenv("SECRET_ARN", "test_secret")
    monkeypatch.setenv("REGION_NAME", "uk-west-1")


def test_connection():
    with patch("database.oracledb.connect"):
        with database.connection() as conn:
            assert conn is not None

        assert conn.closed


def test_failed_connection_to_db():
    database.oracledb.connect = Mock(side_effect=oracledb.Error("Something's wrong"))
    with pytest.raises(database.DatabaseError) as exc_info:
        database.connection().__enter__()

    assert str(exc_info.value) == "Database Error: Something's wrong"


def test_cursor():
    with patch("database.oracledb.connect"):
        with database.cursor() as cursor:
            assert cursor is not None

        assert cursor.closed


def test_failed_cursor():
    database.oracledb.connect.return_value.cursor = Mock(side_effect=oracledb.Error("Something's wrong"))
    with pytest.raises(database.DatabaseError) as exc_info:
        database.cursor().__enter__()

    assert str(exc_info.value) == "Database Error: Something's wrong"


def test_connection_params():
    assert database.connection_params() == {"user": "test", "password": "test", "dsn": "test_host:1521/test_sid"}
