import sqlite3

DB = "memor.db"


def get_conn():
    return sqlite3.connect(DB)


# ======================================
# SAVE MEMORY
# ======================================

def save_memory(
    user_id,
    kategori,
    kunci,
    nilai,
    importance=1
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO memory

        (
            user_id,
            kategori,
            kunci,
            nilai,
            importance
        )

        VALUES (?,?,?,?,?)

    """, (
        user_id,
        kategori,
        kunci,
        nilai,
        importance
    ))

    conn.commit()
    conn.close()


# ======================================
# GET LAST MEMORY
# ======================================

def get_memory(user_id, limit=10):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            kategori,
            kunci,
            nilai

        FROM memory

        WHERE user_id = ?

        ORDER BY
            importance DESC,
            id DESC

        LIMIT ?

    """, (
        user_id,
        limit
    ))

    data = cursor.fetchall()

    conn.close()

    if not data:
        return ""

    hasil = []

    for kategori, kunci, nilai in data:

        hasil.append(
            f"[{kategori}] {kunci}: {nilai}"
        )

    return "\n".join(hasil)


# ======================================
# SEARCH MEMORY
# ======================================

def search_memory(user_id, keyword):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            kategori,
            kunci,
            nilai

        FROM memory

        WHERE
            user_id = ?
            AND
            (
                kunci LIKE ?
                OR nilai LIKE ?
            )

        ORDER BY importance DESC

    """, (
        user_id,
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    data = cursor.fetchall()

    conn.close()

    return data


# ======================================
# DELETE MEMORY
# ======================================

def delete_memory(user_id, kunci):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM memory

        WHERE
            user_id = ?
            AND
            kunci = ?

    """, (
        user_id,
        kunci
    ))

    conn.commit()
    conn.close()