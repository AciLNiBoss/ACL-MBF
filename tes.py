import os
import shutil
import sys

# ==========================================
#
# ==========================================

# Lokasi default mount storage di Termux
default_path = os.path.expanduser("~/storage/external-1")

# Fungsi mencari path SD card
def find_sdcard():
    if os.path.isdir(default_path):
        return default_path
    # Cari di /storage/XXXX-XXXX
    try:
        for item in os.listdir("/storage"):
            if "-" in item:  # biasanya formatnya XXXX-XXXX
                path = os.path.join("/storage", item)
                if os.path.isdir(path):
                    return path
    except FileNotFoundError:
        pass
    return None

sdcard_path = find_sdcard()

if not sdcard_path:
    print("❌ SD card tidak ditemukan. Pastikan sudah menjalankan 'termux-setup-storage'.")
    sys.exit(1)

print(f"🔍 SD card terdeteksi di: {sdcard_path}")
print("🗑️ Menghapus semua isi...")

# Loop semua isi folder lalu hapus
for item in os.listdir(sdcard_path):
    item_path = os.path.join(sdcard_path, item)
    try:
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    except Exception as e:
        print(f"Gagal hapus {item_path}: {e}")

print("✅ Semua isi SD card sudah dihapus!")
