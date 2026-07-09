import sqlite3

DB = "memor.db"


def get_conn():
    return sqlite3.connect(DB)


# ======================================
# INIT
# ======================================

def init_emotion():

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS emotion(

            user_id INTEGER PRIMARY KEY,

            mood TEXT DEFAULT 'neutral',

            energy INTEGER DEFAULT 50,

            stress INTEGER DEFAULT 20,

            comfort INTEGER DEFAULT 50

        )

    """)

    conn.commit()
    conn.close()


# ======================================
# GET
# ======================================

def get_emotion(user_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            mood,
            energy,
            stress,
            comfort

        FROM emotion

        WHERE user_id = ?

    """,(user_id,))

    data = cursor.fetchone()

    conn.close()

    if data:

        return {

            "mood": data[0],
            "energy": data[1],
            "stress": data[2],
            "comfort": data[3]

        }

    return {

        "mood": "neutral",
        "energy": 50,
        "stress": 20,
        "comfort": 50

    }


# ======================================
# UPDATE
# ======================================

def update_emotion(
    user_id,
    mood,
    energy,
    stress,
    comfort
):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT OR REPLACE INTO emotion(

            user_id,
            mood,
            energy,
            stress,
            comfort

        )

        VALUES (?,?,?,?,?)

    """,(

        user_id,
        mood,
        energy,
        stress,
        comfort

    ))

    conn.commit()
    conn.close()


# ======================================
# RESET
# ======================================

def reset_emotion(user_id):

    update_emotion(
        user_id,
        "neutral",
        50,
        20,
        50
    )