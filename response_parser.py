import json


# ======================================
# EXTRACT JSON
# ======================================

def extract_json(text):

    try:

        start = text.find("{")
        end = text.rfind("}") + 1


        if start == -1 or end == 0:
            return None


        clean = text[start:end]

        return json.loads(clean)


    except Exception:

        return None



# ======================================
# PARSE RESPONSE
# ======================================

def parse_response(raw):

    data = extract_json(raw)


    if not data:

        return {

            "reply": raw,

            "memory": None,

            "emotion": None

        }


    return {

        "reply": data.get(
            "reply",
            raw
        ),

        "memory": data.get(
            "memory"
        ),

        "emotion": data.get(
            "emotion"
        )

    }



# ======================================
# MEMORY CHECK
# ======================================

def get_memory_update(parsed):

    return parsed.get(
        "memory"
    )



# ======================================
# EMOTION CHECK
# ======================================

def get_emotion_update(parsed):

    return parsed.get(
        "emotion"
    )