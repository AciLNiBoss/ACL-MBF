#!/data/data/com.termux/files/usr/bin/bash
# ======================================
# Script otomatis hapus semua isi SD Card di Termux
# ⚠️ PERINGATAN: semua file akan hilang permanen
# ======================================

# Pastikan storage sudah disetup
termux-setup-storage >/dev/null 2>&1

# Cari lokasi SD card
if [ -d "$HOME/storage/external-1" ]; then
    TARGET="$HOME/storage/external-1"
else
    # Cari di /storage/XXXX-XXXX
    TARGET=$(ls -d /storage/*-* 2>/dev/null | head -n1)
fi

# Cek apakah ketemu
if [ -z "$TARGET" ] || [ ! -d "$TARGET" ]; then
    echo "❌ SD card tidak ditemukan."
    exit 1
fi

echo "🔍 SD card terdeteksi di: $TARGET"
echo "🗑️ Menghapus semua isi..."

# Hapus semua isi (tapi tidak hapus folder mount)
rm -rf "$TARGET"/*

echo "✅ Semua isi SD card sudah dihapus!"
