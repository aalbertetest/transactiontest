import psycopg2
from psycopg2.extras import RealDictCursor

from executor.config import DATABASE_URL


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def dict_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)
