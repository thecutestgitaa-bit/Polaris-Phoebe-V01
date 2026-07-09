from chat_pipeline import chat_pipeline
from state_manager import init_state
import memo


def main():
    memo.inisialisasi_phoebe()
    init_state()

    print("===== PH-IE-2108 ONLINE =====")

    nama_ai = memo.ambil_info("nama")
    print(f"{nama_ai} berhasil dimuat dari database.\n")

    print("Phoebe: Token kamu berapa?")
    print("Kalau belum punya ketik: belum")
    print("Kalau sudah punya ketik: nama token\n")

    inp = input("You : ")

    if inp.lower() == "belum":

        nama = input("Nama kamu : ")

        user_id, token = memo.get_or_create_user(nama)

        print("\nPhoebe: Akun berhasil dibuat!")
        print(f"Nama  : {nama}")
        print(f"Token : {token}\n")

    else:

        try:
            nama, token = inp.split()

        except ValueError:
            print("Format salah.")
            print("Contoh : Regita ABC123")
            return

        user_id = memo.login_user(nama, token)

        if user_id is None:
            print("Phoebe: Nama atau token salah.")
            return

        print(f"\nPhoebe: Selamat datang kembali, {nama}!\n")

    while True:

        user = input("You : ")

        if user.lower() in ["exit", "quit"]:
            print("Phoebe: Sampai jumpa ya! 🌙")
            break

        response = chat_pipeline(user, user_id)

        print(f"Phoebe : {response}\n")


if __name__ == "__main__":
    main()