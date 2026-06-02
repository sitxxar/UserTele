import os
import sys
import asyncio
import random
import argparse
from modules.config_manager import load_config
from modules.tg_client import get_client, init_session
from modules.checker import check_username, STATUS_AVAILABLE, STATUS_TAKEN, STATUS_INVALID, STATUS_FLOOD, STATUS_ERROR

# Warna ANSI untuk output CLI
G = "\033[92m" # Hijau
R = "\033[91m" # Merah
Y = "\033[93m" # Kuning
C = "\033[96m" # Cyan
M = "\033[95m" # Magenta
B = "\033[1m"  # Bold
W = "\033[0m"  # Reset

def print_banner():
    banner = f"""{C}
╔╦╗╔═╗╦  ╔═╗╔═╗╦═╗╔═╗╔╦╗  ╔═╗╦  ╦  ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗
 ║ ║╣ ║  ║╣ ║ ╦╠╦╝╠═╣║║║  ║  ║  ║  ║  ╠═╣║╣ ║  ╠╩╗║╣ ╠╦╝
 ╩ ╚═╝╩═╝╚═╝╚═╝╩╚═╩ ╩╩ ╩  ╚═╝╩═╝╩  ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═
            {Y}Telegram Username Checker By SITXXAR{W}
    """
    print(banner)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Alat pengecek ketersediaan username Telegram menggunakan Telethon resmi.")
    parser.add_argument("-f", "--file", type=str, default="usernames.txt",
                        help="Path ke file berisi daftar username (default: usernames.txt)")
    parser.add_argument("-u", "--usernames", type=str,
                        help="Daftar username langsung dipisahkan dengan koma (contoh: user1,user2)")
    parser.add_argument("-o", "--output", type=str, default="available.txt",
                        help="File hasil untuk menyimpan username yang tersedia (default: available.txt)")
    parser.add_argument("--min-delay", type=float,
                        help="Delay minimum antar pengecekan dalam detik (override config.json)")
    parser.add_argument("--max-delay", type=float,
                        help="Delay maksimum antar pengecekan dalam detik (override config.json)")
    return parser.parse_args()

def load_usernames_from_file(file_path):
    if not os.path.exists(file_path):
        # Buat file kosong dengan template jika belum ada
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("# Masukkan username Telegram yang ingin dicek di sini\n")
            f.write("# Satu username per baris. Karakter '#' di awal baris diabaikan.\n")
            f.write("username_contoh1\n")
            f.write("username_contoh2\n")
        print(f"[*] File {file_path} tidak ditemukan. File kosong baru telah dibuat.")
        print(f"[!] Silakan isi file {file_path} dengan daftar username Anda lalu jalankan ulang program.")
        return []
    
    usernames = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            usernames.append(line)
    return usernames

async def process_check(client, username, available_file, min_delay, max_delay):
    """
    Mengecek username dengan penanganan otomatis jika terkena FloodWaitError.
    """
    while True:
        status, info = await check_username(client, username)
        
        if status == STATUS_FLOOD:
            # Info berisi jumlah detik sleep yang diminta Telegram
            wait_seconds = int(info)
            print(f"[{M}FLOOD{W}] Batas request Telegram tercapai. Tidur otomatis selama {Y}{wait_seconds}{W} detik...")
            await asyncio.sleep(wait_seconds)
            print(f"[*] Bangun dari tidur, mencoba kembali mengecek @{username}...")
            continue  # Mengulangi pengecekan username yang sama
            
        elif status == STATUS_AVAILABLE:
            print(f"[{G}AVAILABLE{W}] {B}@{username}{W} -> Tersedia!")
            # Simpan secara realtime ke file output
            with open(available_file, 'a', encoding='utf-8') as f:
                f.write(f"{username}\n")
            break
            
        elif status == STATUS_TAKEN:
            print(f"[{R}TAKEN{W}] @{username} -> Sudah digunakan.")
            break
            
        elif status == STATUS_INVALID:
            print(f"[{Y}INVALID{W}] @{username} -> {info}")
            break
            
        else: # STATUS_ERROR
            print(f"[{R}ERROR{W}] @{username} -> {info}")
            break

    # Jeda acak antar request untuk meminimalkan risiko rate limit
    delay = random.uniform(min_delay, max_delay)
    await asyncio.sleep(delay)

async def main():
    print_banner()
    args = parse_arguments()
    
    # 1. Muat Konfigurasi API
    try:
        config = load_config()
    except Exception as e:
        print(f"[{R}ERROR{W}] Konfigurasi gagal dimuat: {e}")
        sys.exit(1)
        
    api_id = config["api_id"]
    api_hash = config["api_hash"]
    
    # Tentukan delay (argumen CLI meng-override config.json)
    min_delay = args.min_delay if args.min_delay is not None else config["min_delay"]
    max_delay = args.max_delay if args.max_delay is not None else config["max_delay"]
    
    # 2. Dapatkan Daftar Username
    usernames = []
    if args.usernames:
        usernames = [u.strip() for u in args.usernames.split(",") if u.strip()]
    else:
        usernames = load_usernames_from_file(args.file)
        if not usernames:
            print(f"[-] Tidak ada username yang diproses.")
            sys.exit(0)
            
    print(f"[*] Jumlah username untuk dicek: {B}{len(usernames)}{W}")
    print(f"[*] Konfigurasi Jeda: {min_delay} - {max_delay} detik per request.\n")
    
    # 3. Inisialisasi dan Autentikasi Client
    client = get_client(api_id, api_hash)
    try:
        await init_session(client)
    except Exception as e:
        print(f"\n[{R}ERROR{W}] Gagal autentikasi ke Telegram: {e}")
        sys.exit(1)
        
    print(f"\n{B}[+] Memulai proses pengecekan...{W}")
    print(f"[*] Hasil username tersedia akan disimpan di: {B}{args.output}{W}\n")
    
    # Bersihkan file output agar tidak bertumpuk jika user ingin yang bersih, 
    # namun demi keselamatan, kita akan buat file baru atau membiarkannya di-append.
    # Di sini kita gunakan mode append ('a') di fungsi process_check agar data tidak hilang jika terhenti di tengah jalan.
    
    for index, username in enumerate(usernames, 1):
        clean_username = username.lstrip('@').strip()
        print(f"[{index}/{len(usernames)}] Mengecek {B}@{clean_username}{W}...", end="\r")
        await process_check(client, clean_username, args.output, min_delay, max_delay)
        
    print(f"\n{G}{B}[+] Selesai! Pengecekan username selesai dilakukan.{W}")
    if os.path.exists(args.output) and os.path.getsize(args.output) > 0:
        print(f"[*] Username tersedia telah disimpan di file {C}{args.output}{W}")
    else:
        print("[-] Tidak ada username yang tersedia ditemukan.")

if __name__ == "__main__":
    # Aktifkan dukungan warna ANSI di terminal Windows CMD/PowerShell
    if sys.platform == "win32":
        import os
        os.system("")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{R}[!] Program dihentikan paksa oleh pengguna (KeyboardInterrupt).{W}")
        sys.exit(0)
