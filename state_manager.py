import sqlite3


DB = "memor.db"


# ======================================
# DATABASE CONNECTION
# ======================================

def get_conn():
    return sqlite3.connect(DB)


# ======================================
# INIT STATE
# ======================================

def init_state():

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS phoebe_state(

        id INTEGER PRIMARY KEY,

        mood TEXT,
        energy INTEGER,
        stress INTEGER,
        comfort INTEGER

    )
    """)


    cursor.execute("""
    SELECT id FROM phoebe_state
    WHERE id = 1
    """)

    exists = cursor.fetchone()


    if not exists:

        cursor.execute("""
        INSERT INTO phoebe_state
        (
            id,
            mood,
            energy,
            stress,
            comfort
        )

        VALUES
        (
            1,
            'happy',
            80,
            20,
            70
        )
        """)


    conn.commit()
    conn.close()



# ======================================
# GET STATE
# ======================================

def get_state():

    conn = get_conn()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT
        mood,
        energy,
        stress,
        comfort

    FROM phoebe_state

    WHERE id = 1
    """)


    data = cursor.fetchone()

    conn.close()


    if not data:
        init_state()
        return get_state()


    return {

        "mood": data[0],
        "energy": data[1],
        "stress": data[2],
        "comfort": data[3]

    }



# ======================================
# UPDATE STATE
# ======================================

def update_state(
    mood=None,
    energy=None,
    stress=None,
    comfort=None
):

    current = get_state()


    if mood:
        current["mood"] = mood

    if energy is not None:
        current["energy"] = energy

    if stress is not None:
        current["stress"] = stress

    if comfort is not None:
        current["comfort"] = comfort



    conn = get_conn()
    cursor = conn.cursor()


    cursor.execute("""
    UPDATE phoebe_state

    SET
        mood=?,
        energy=?,
        stress=?,
        comfort=?

    WHERE id=1

    """,
    (
        current["mood"],
        current["energy"],
        current["stress"],
        current["comfort"]
    ))


    conn.commit()
    conn.close()



# ======================================
# CONTEXT FORMAT
# ======================================

def state_to_text():

    state = get_state()


    return f"""
Mood:
{state['mood']}

Energy:
{state['energy']}/100

Stress:
{state['stress']}/100

Comfort:
{state['comfort']}/100
"""