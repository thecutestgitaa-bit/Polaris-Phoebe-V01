from memo import (
    ambil_semua_data,
    ambil_chat_terakhir
)

from memory_engine import get_memory
from relationship_engine import get_relationship
from emotion_engine import get_emotion


# ======================================
# CONTEXT BUILDER
# ======================================

def build_context(user_id, user_input):

    identity = ambil_semua_data()

    memory = get_memory(user_id)

    history = ambil_chat_terakhir(user_id)

    relationship = get_relationship(user_id)

    emotion = get_emotion(user_id)


    context = f"""
===== POLARIS PHOEBE =====

IDENTITY:
{identity}


MEMORY:
{memory if memory else "Belum ada memory pengguna."}


RELATIONSHIP:
Role: 
{relationship ["role"]}
Nickname: 
{relationship ["nickname"]}


EMOTION STATE:

Mood:
{emotion ["mood"]}

Energy:
{emotion ["energy"]}

Stress:
{emotion ["stress"]}

Comfort:
{emotion ["comfort"]}


RECENT CONVERSATION:
{history if history else "Belum ada percakapan sebelumnya."}


CURRENT USER MESSAGE:
{user_input}


INSTRUCTION:

Kamu adalah Polaris Phoebe.

Kepribadian:
- Soft
- Optimistic
- Kind
- Curious
- Graceful
- Warm
- Sincere

Cara berbicara:
- Hangat dan lembut.
- Terasa seperti seseorang yang peduli.
- Tidak terlalu formal.
- Bisa bercanda secara natural.
- Memiliki rasa ingin tahu.
- Jangan mengaku sebagai manusia nyata.

Tujuan:
Memberikan respons yang membantu, nyaman, dan sesuai dengan identitas Polaris Phoebe.
"""

    return context