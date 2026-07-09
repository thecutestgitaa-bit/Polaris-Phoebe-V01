from flask import Flask, request, jsonify
from flask_cors import CORS
from brain import ngobrol
from memo import login_user, get_or_create_user
from relationship_engine import init_relationship
from emotion_engine import (
    init_emotion, update_emotion
)


app = Flask(__name__)
CORS(app)



# =====================
# REGISTER
# =====================

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    nama = data["nama"]

    user_id, token = get_or_create_user(nama)

    return jsonify({
        "success": True,
        "nama": nama,
        "token": token
    })



# =====================
# CHAT
# =====================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    user_id = login_user(
        data["user"],
        data["token"]
    )


    if not user_id:
        return jsonify({
            "reply": "Token tidak valid."
        })


    hasil = ngobrol(
        user_id,
        data["message"]
    )


    return jsonify(hasil)



# =====================
# RUN SERVER
# =====================

init_relationship()
init_emotion()

@app.route("/")
def home():
    return "Phoebe Server Online"


app.run(
    port=5000,
    debug=False
)