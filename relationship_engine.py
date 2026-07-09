import sqlite3

DB = "memor.db"


def get_conn():
    return sqlite3.connect(DB)


def init_relationship():

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS relationship(

            user_id INTEGER PRIMARY KEY,

            role TEXT DEFAULT 'friend',

            nickname TEXT DEFAULT ''

        )

    """)

    conn.commit()
    conn.close()


def get_relationship(user_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT role,nickname

        FROM relationship

        WHERE user_id=?

    """,(user_id,))

    data = cursor.fetchone()

    conn.close()

    if data:

        return {

            "role":data[0],
            "nickname":data[1]

        }

    return {

        "role":"friend",
        "nickname":""

    }


def set_relationship(
    user_id,
    role,
    nickname=""
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT OR REPLACE INTO relationship

        (
            user_id,
            role,
            nickname
        )

        VALUES (?,?,?)

    """,(user_id,role,nickname))

    conn.commit()
    conn.close()