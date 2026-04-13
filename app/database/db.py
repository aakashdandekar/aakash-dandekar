"""Database connection and schema initialisation."""
import sqlite3
from ..core.config import settings


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # better concurrent reads
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


_SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    abbr        TEXT    NOT NULL,
    description TEXT    NOT NULL,
    tags        TEXT    NOT NULL DEFAULT '[]',
    stack       TEXT    NOT NULL DEFAULT '[]',
    link        TEXT    NOT NULL DEFAULT '#',
    color       TEXT    NOT NULL DEFAULT 'cyan',
    featured    INTEGER NOT NULL DEFAULT 0,
    sort_order  INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS services (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT    NOT NULL,
    list_items  TEXT    NOT NULL DEFAULT '[]',
    sort_order  INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS skill_groups (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    color       TEXT    NOT NULL DEFAULT 'cyan',
    skills      TEXT    NOT NULL DEFAULT '[]',
    sort_order  INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS about_chips (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS about_values (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    num         TEXT    NOT NULL,
    title       TEXT    NOT NULL,
    description TEXT    NOT NULL,
    sort_order  INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS contact_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    abbr        TEXT    NOT NULL,
    label       TEXT    NOT NULL,
    href        TEXT    NOT NULL,
    display     TEXT    NOT NULL,
    is_external INTEGER NOT NULL DEFAULT 1,
    sort_order  INTEGER NOT NULL DEFAULT 0
);
"""


def init_db() -> None:
    from .seed import seed_if_empty
    conn = get_db()
    conn.executescript(_SCHEMA)
    seed_if_empty(conn)
    conn.commit()
    conn.close()
