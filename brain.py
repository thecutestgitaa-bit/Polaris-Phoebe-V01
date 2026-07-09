from context_builder import build_context
from otak import ngobrol_llm
from memory_engine import save_memory
from memo import simpan_chat
import json


def ngobrol(user_id, message):

    # simpan pesan user
    simpan_chat(
        user_id,
        "user",
        message
    )


    # buat context Phoebe
    context = build_context(
        user_id,
        message
    )


    # kirim ke LLM
    response = ngobrol_llm(
        context
    )


    # ubah JSON dari Phoebe
    data = json.loads(response)


    # simpan jawaban Phoebe
    simpan_chat(
        user_id,
        "phoebe",
        data["reply"]
    )


    # simpan memory kalau Phoebe membuat memory baru
    memory = data.get("memory")


    if memory and memory.get("save"):

        save_memory(
            user_id,
            "conversation",
            memory.get("key"),
            memory.get("value"),
            memory.get("importance", 1)
        )


    return data