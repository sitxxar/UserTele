import os
from telethon import TelegramClient

def get_client(api_id, api_hash, session_name="tg_checker_session"):
    """
    Menginisialisasi objek TelegramClient menggunakan session file di folder project.
    """
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    session_path = os.path.join(project_dir, session_name)
    
    # Inisialisasi client
    client = TelegramClient(session_path, int(api_id), api_hash)
    return client

async def init_session(client):
    """
    Memulai client dan melakukan autentikasi jika diperlukan.
    Menggunakan start() bawaan Telethon yang menangani input nomor handphone,
    OTP, dan password 2FA secara interaktif melalui terminal.
    """
    print("[*] Menghubungkan ke API Telegram...")
    await client.start()
    print("[+] Berhasil terhubung dan terautentikasi!")
