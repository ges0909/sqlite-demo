import sqlite3

import pytest

DATABASE = "test.db"


@pytest.fixture(scope="module")
def connection():
    return sqlite3.connect(DATABASE)


def test_sqlite_basic():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS PERSONS (
        first VARCHAR(20), 
        last VARCHAR(30), 
        date_of_birth DATE
    )"""
    cursor.execute(sql)
    connection.commit()

    cursor.execute('INSERT INTO PERSONS VALUES("Heike", "Zimmermann", "1962-05-13")')
    connection.commit()

    connection.close()


def test_create_table(connection):
    with connection:  # context manager to commit or rollback, but NOT to close connection
        connection.execute(  # shortcut for cursor.execute
            """
            CREATE TABLE IF NOT EXISTS USERS (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER
            )
            """
        )


def test_insert_many_rows(connection):
    sql = "INSERT INTO USERS (id, name, age) VALUES(?, ?, ?)"
    values = [
        (1, "Alice", 21),
        (2, "Bob", 22),
        (3, "Chris", 23),
    ]
    with connection:
        connection.executemany(sql, values)
    assert connection.total_changes == 3


def test_select_rows(connection):
    with connection:
        rows = connection.execute(
            "SELECT * FROM USERS WHERE age <= ?", (22,)
        ).fetchall()
        assert rows == [
            (1, "Alice", 21),
            (2, "Bob", 22),
        ]


def test_update_row(connection):
    with connection:
        connection.execute(
            "UPDATE USERS SET name = ? WHERE name == ?",
            ("Bobby", "Bob"),
        )


def test_delete_row(connection):
    with connection:
        connection.execute("DELETE FROM USERS WHERE name == ?", ("Bob",))


def test_drop_table(connection):
    with connection:
        connection.execute("DROP TABLE IF EXISTS USERS")
        connection.execute("DROP TABLE IF EXISTS PERSONS")
