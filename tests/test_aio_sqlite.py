import aiosqlite
import pytest

DATABASE = "aio_test.db"


@pytest.mark.asyncio
async def test_sqlite_basic_use():

    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS PERSONS (
                first VARCHAR(20), 
                last VARCHAR(30), 
                date_of_birth DATE
            )"""
        )
        await db.commit()

        await db.execute(
            """INSERT INTO PERSONS VALUES("Heike", "Zimmermann", "1962-05-13")"""
        )
        await db.commit()
        assert db.total_changes > 0

        async with db.execute("SELECT * FROM PERSONS") as cursor:
            async for row in cursor:
                first = row[0]
                last = row[1]
                date_of_birth = row[2]

        await db.execute("DROP TABLE IF EXISTS PERSONS")
        await db.commit()
