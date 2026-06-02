import re
from telethon import TelegramClient, functions
from telethon.errors import UsernameInvalidError, FloodWaitError

# Konstanta Status
STATUS_AVAILABLE = "AVAILABLE"
STATUS_TAKEN = "TAKEN"
STATUS_INVALID = "INVALID"
STATUS_FLOOD = "FLOOD_LIMIT"
STATUS_ERROR = "ERROR"

def validate_username_format(username: str) -> bool:
    """
    Melakukan validasi format username Telegram secara offline sebelum memanggil API.
    Aturan Telegram:
    - Panjang 5 - 32 karakter.
    - Karakter diperbolehkan: a-z, 0-9, dan underscore (_).
    - Harus diawali dengan huruf (tidak boleh angka atau underscore di awal).
    - Case-insensitive.
    """
    username = username.lstrip('@')
    if not (5 <= len(username) <= 32):
        return False
    # Regex untuk memastikan diawali huruf, diikuti huruf/angka/underscore
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", username):
        return False
    return True

async def check_username(client: TelegramClient, username: str):
    """
    Mengecek status ketersediaan username Telegram via API menggunakan CheckUsernameRequest.
    Mengembalikan tuple: (STATUS, info_tambahan)
    """
    username = username.lstrip('@').strip()
    
    # 1. Validasi format offline
    if not validate_username_format(username):
        return STATUS_INVALID, "Format tidak valid (harus 5-32 char, diawali huruf, hanya alfanumerik & _)"
        
    # 2. Pengecekan via Telegram API menggunakan CheckUsernameRequest
    try:
        is_available = await client(functions.account.CheckUsernameRequest(username=username))
        if is_available:
            return STATUS_AVAILABLE, "Tersedia (AVAILABLE)"
        else:
            return STATUS_TAKEN, "Sudah digunakan (TAKEN)"
    except UsernameInvalidError:
        # Username invalid atau sudah diblokir/direserve/fragment oleh Telegram
        return STATUS_INVALID, "Ditolak/Reserved oleh Telegram (INVALID)"
    except FloodWaitError as e:
        # Kembalikan status FLOOD dan durasi tunggunya dalam detik
        return STATUS_FLOOD, e.seconds
    except Exception as e:
        # Error tidak terduga lainnya
        return STATUS_ERROR, f"Error: {str(e)}"
