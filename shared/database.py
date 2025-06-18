from contextlib import contextmanager
import logging
from typing import Any, Generator

import oracledb
import os

from oracledb import Cursor, Connection


class DatabaseError(Exception):
    """Raised when there is an error from the database"""


@contextmanager
def connection() -> Generator[Connection, Any, None]:
    try:
        conn = oracledb.connect(**connection_params())
        try:
            yield conn
        finally:
            conn.close()
    except oracledb.Error as e:
        logging.error("Database Error: %s", e)
        raise DatabaseError(f"Database Error: {str(e)}") from e


@contextmanager
def cursor() -> Generator[Cursor, Any, None]:
    with connection() as conn:
        cur = conn.cursor()
        try:
            yield cur
        finally:
            cur.close()


def connection_params() -> dict:
    db_user = os.getenv("DATABASE_USER")
    db_password = os.getenv("DATABASE_PASSWORD")
    host: str = os.environ["DATABASE_HOST"]
    port: str = os.getenv("DATABASE_PORT", "1521")
    sid: str = os.environ["DATABASE_SID"]
    dsn_tns = f"{host}:{port}/{sid}"

    return {"user": db_user, "password": db_password, "dsn": dsn_tns}
