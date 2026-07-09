from context_builder import build_context
from otak import ngobrol_llm

from response_parser import (
    parse_response,
    get_emotion_update,
    get_memory_update
)

from state_manager import update_state

from memory_engine import save_memory

from memo import simpan_chat



# ======================================
# CHAT PIPELINE
# ======================================

def chat_pipeline(user_input, user_id):


    # 1. BUILD CONTEXT

    context = build_context(
        user_id,
        user_input
    )



    # 2. SEND TO LLM

    raw = ngobrol_llm(
        context
    )



    # 3. PARSE RESPONSE

    data = parse_response(
        raw
    )


    if not data:

        return "Maaf, terjadi error."



    reply = data["reply"]



    # 4. SAVE CHAT

    simpan_chat(
        user_id,
        "user",
        user_input
    )


    simpan_chat(
        user_id,
        "assistant",
        reply
    )



    # 5. SAVE MEMORY IF EXISTS

    memory = get_memory_update(
        data
    )


    if memory:

        if memory.get("save"):

            save_memory(

                user_id,

                "conversation",

                memory.get("key"),

                memory.get("value"),

                memory.get(
                    "importance",
                    1
                )

            )



    # 6. UPDATE EMOTION

    emotion = get_emotion_update(
        data
    )


    if emotion:

        update_state(

            mood=emotion.get(
                "mood"
            ),

            energy=emotion.get(
                "energy"
            ),

            stress=emotion.get(
                "stress"
            ),

            comfort=emotion.get(
                "comfort"
            )

        )



    return reply