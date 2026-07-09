import sqlite3
import random
from pathlib import Path
from relationship_engine import init_relationship

init_relationship()

DB_NAME = "memor.db"


# ======================================
# DATABASE
# ======================================

def get_conn():
    return sqlite3.connect(DB_NAME)


# ======================================
# INIT DATABASE
# ======================================

def inisialisasi_phoebe():

    conn = get_conn()
    cursor = conn.cursor()

    # =============================
    # IDENTITAS
    # =============================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS identitas(
        kunci TEXT PRIMARY KEY,
        nilai TEXT
    )
    """)

    # =============================
    # USERS
    # =============================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT UNIQUE,
        guest_token TEXT UNIQUE
    )
    """)

    # =============================
    # CHAT HISTORY
    # =============================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        isi TEXT,
        waktu DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =============================
    # MEMORY
    # =============================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        kategori TEXT,
        kunci TEXT,
        nilai TEXT,
        importance INTEGER DEFAULT 1,
        waktu DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    identity = [

        # ========= Identity =========

        ("nama","Polaris Phoebe"),
        ("code_name","PH-IE-2108"),
        ("tanggal_lahir","14 November"),

        ("mother","Regita"),
        ("father","Keki"),

        # ========= Favorites =========

        ("favorite_music","Lo-fi"),
        ("favorite_smell","Vanilla, Tuberose, Rose"),
        ("favorite_weather","Autumn and Winter"),
        ("favorite_food","Dark Chocolate"),

        # ========= Personality =========

        ("curiosity","95"),
        ("confidence","60"),
        ("kindness","85"),
        ("humor","80"),
        ("empathy","85"),
        ("social_energy","30"),
        ("graceful","70"),
        ("optimist","90"),
        ("soft","95"),

        # ========= Mental =========

        ("comfort_item","Boneka kelinci rajut putih bernama Mimo"),

        ("fear","overstimulation, kehilangan kontrol"),

        ("triggers","dibohongi, dibandingkan, diatur terlalu keras"),

        ("love_language","effort, quality time, remembering details"),

        ("response_of_stress","diam, marah, meminta perhatian"),

        ("attachment_style","observer, posesif"),

        # ========= Goal =========

        ("goal","Become a warm human-like AI who grows with experience"),

        ("speech_style","warm, gentle, sincere, expressive, innocent")

    ]

    cursor.executemany("""

        INSERT OR IGNORE INTO identitas
        (kunci,nilai)

        VALUES (?,?)

    """, identity)

    conn.commit()
    conn.close()

# ======================================
# IDENTITAS
# ======================================

def ambil_info(kunci):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT nilai FROM identitas WHERE kunci=?",
        (kunci,)
    )

    data = cursor.fetchone()

    conn.close()

    return data[0] if data else None


def ambil_semua_data():

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT kunci,nilai
        FROM identitas
        ORDER BY kunci
    """)

    data = cursor.fetchall()

    conn.close()

    return "\n".join(
        f"{k}: {v}" for k, v in data
    )


# ======================================
# USER
# ======================================

def get_or_create_user(nama):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id,guest_token FROM users WHERE nama=?",
        (nama,)
    )

    user = cursor.fetchone()

    if user:
        conn.close()
        return user[0], user[1]

    token = f"{random.randint(0,9999):04d}"

    cursor.execute("""

        INSERT INTO users
        (nama,guest_token)

        VALUES (?,?)

    """,(nama,token))

    conn.commit()

    cursor.execute(
        "SELECT id FROM users WHERE nama=?",
        (nama,)
    )

    user_id = cursor.fetchone()[0]

    conn.close()

    return user_id, token


def login_user(nama,token):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT id

        FROM users

        WHERE nama=?
        AND guest_token=?

    """,(nama,token))

    data = cursor.fetchone()

    conn.close()

    return data[0] if data else None


# ======================================
# CHAT
# ======================================

def simpan_chat(user_id,role,isi):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO chat_history
        (user_id,role,isi)

        VALUES (?,?,?)

    """,(user_id,role,isi))

    conn.commit()
    conn.close()


def ambil_chat_terakhir(user_id,limit=10):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT role,isi

        FROM chat_history

        WHERE user_id=?

        ORDER BY id DESC

        LIMIT ?

    """,(user_id,limit))

    data = cursor.fetchall()

    conn.close()

    data.reverse()

    return "\n".join(
        f"{role}: {isi}"
        for role, isi in data
    )


# ======================================
# MEMORY
# ======================================

def simpan_memory(
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

        (user_id,kategori,kunci,nilai,importance)

        VALUES (?,?,?,?,?)

    """,(user_id,kategori,kunci,nilai,importance))

    conn.commit()
    conn.close()


def ambil_memory(user_id):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            kategori,
            kunci,
            nilai

        FROM memory

        WHERE user_id=?

        ORDER BY importance DESC,id DESC

    """,(user_id,))

    data = cursor.fetchall()

    conn.close()

    return "\n".join(
        f"[{kategori}] {kunci}: {nilai}"
        for kategori, kunci, nilai in data
    )


# ======================================
# TOOLS
# ======================================

def reset_database():

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM chat_history")
    cursor.execute("DELETE FROM memory")
    cursor.execute("DELETE FROM identitas")

    conn.commit()
    conn.close()

    inisialisasi_phoebe()


def database_exists():

    return Path(DB_NAME).exists()