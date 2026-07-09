from flask import Flask, request, jsonify, send_file

from chat_pipeline import chat_pipeline
from state_manager import init_state
import memo

app = Flask(__name__)

# Inisialisasi Phoebe
memo.inisialisasi_phoebe()
init_state()

# Menyimpan user yang sedang login
CURRENT_USER = None


# ==========================
# HALAMAN WEBSITE
# ==========================

@app.route("/")
def home():
    return send_file("index.html")


@app.route("/style.css")
def style():
    return send_file("style.css")


@app.route("/script.js")
def script():
    return send_file("script.js")


# ==========================
# REGISTER
# ==========================

@app.route("/register", methods=["POST"])
def register():

    global CURRENT_USER

    data = request.json

    nama = data["nama"]

    user_id, token = memo.get_or_create_user(nama)

    CURRENT_USER = user_id

    return jsonify({
        "success": True,
        "token": token
    })


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["POST"])
def login():

    global CURRENT_USER

    data = request.json

    nama = data["nama"]
    token = data["token"]

    user_id = memo.login_user(nama, token)

    if user_id is None:

        return jsonify({
            "success": False
        })

    CURRENT_USER = user_id

    return jsonify({
        "success": True
    })


# ==========================
# CHAT
# ==========================

@app.route("/chat", methods=["POST"])
def chat():

    global CURRENT_USER

    if CURRENT_USER is None:

        return jsonify({
            "reply": "Silakan login terlebih dahulu."
        })

    data = request.json

    pesan = data["message"]

    jawaban = chat_pipeline(pesan, CURRENT_USER)

    return jsonify({
        "reply": jawaban
    })


# ==========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )