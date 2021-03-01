import sqlite3

import pytest

DATABASE = "mytest.db"


@pytest.fixture(scope="module")
def con():
    return sqlite3.connect(DATABASE)


def test_sqlite_connect():
    connection = sqlite3.connect(DATABASE)
    assert connection is not None
    connection.close()


@pytest.mark.first
def test_create_table(con):
    with con:
        con.execute(
            """
            CREATE TABLE USER (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER
            )
            """
        )


@pytest.mark.second
def test_insert_multiple_rows(con):
    sql = "INSERT INTO USER (id, name, age) values(?, ?, ?)"
    data = [
        (1, "Alice", 21),
        (2, "Bob", 22),
        (3, "Chris", 23),
    ]
    with con:
        con.executemany(sql, data)


@pytest.mark.third
def test_select_row(con):
    with con:
        data = con.execute("SELECT * FROM USER WHERE age <= 22")
        assert tuple(data) == (
            (1, "Alice", 21),
            (2, "Bob", 22),
        )


@pytest.mark.skip
@pytest.mark.last
def test_drop_table(con):
    with con:
        con.execute("DROP TABLE USER")
