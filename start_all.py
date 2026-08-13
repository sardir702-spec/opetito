import subprocess
import threading
import time
import re
import os
import sys
import platform
import urllib.request

# Skript o'zi joylashgan papkani aniqlash
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Windows konsolda emoji crashni oldini olish
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# Eski jarayonlarni tozalash (port 8080 va bot conflict oldini olish)
print("Eski jarayonlar tekshirilmoqda...")
if platform.system().lower() == 'windows':
    try:
        # Port 8080 ni band qilgan jarayonni o'ldirish
        result = subprocess.run(
            ["netstat", "-ano"], capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if ":8080" in line and "LISTENING" in line:
                parts = line.strip().split()
                pid = parts[-1]
                if pid.isdigit() and int(pid) != os.getpid():
                    subprocess.run(["taskkill", "/F", "/PID", pid],
                                   capture_output=True)
                    print(f"Port 8080 bo'shatildi (PID: {pid})")
    except Exception as e:
        print(f"Tozalashda xatolik (e'tiborsiz): {e}")
time.sleep(1)

# Server muhitini aniqlash (Render, Railway va h.k.)
if os.environ.get('RENDER_EXTERNAL_URL'):
    url = os.environ.get('RENDER_EXTERNAL_URL')
    print(f"[SERVER] Render serveri aniqlandi! URL: {url}")
elif os.environ.get('RAILWAY_STATIC_URL'):
    url = f"https://{os.environ.get('RAILWAY_STATIC_URL')}"
    print(f"[SERVER] Railway serveri aniqlandi! URL: {url}")
else:
    # Mahalliy server yoki VPS uchun Cloudflare Tunnel ishlatish
    print("Cloudflare Tunnel (trycloudflare) tayyorlanmoqda...")
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == 'windows':
        print("Windows aniqlandi. Localtunnel ishga tushirilmoqda (Port 8080)...")
        lt_proc = subprocess.Popen(
            ["npx", "localtunnel", "--port", "8080"], 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            text=True, shell=True
        )
        url = None
        for line in iter(lt_proc.stdout.readline, ''):
            print("LT:", line.strip())
            match = re.search(r'https://[\w-]+\.loca\.lt', line)
            if match:
                url = match.group(0)
                break
            if "your url is:" in line.lower():
                parts = line.split("your url is:")
                if len(parts) > 1:
                    url = parts[1].strip()
                    break
        if not url:
            print("Localtunnel ishga tushmadi!")
            lt_proc.kill()
            exit(1)
            
        def read_cf_output():
            for l in iter(lt_proc.stdout.readline, ''):
                pass
        threading.Thread(target=read_cf_output, daemon=True).start()

    else:
        # Linux/Mac uchun Cloudflare
        binary_name = "cloudflared"
        if 'arm' in machine or 'aarch64' in machine:
            binary_url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
        else:
            binary_url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"

        if not os.path.exists(binary_name):
            print(f"[{binary_name}] yuklanmoqda... (Kuting)")
            try:
                urllib.request.urlretrieve(binary_url, binary_name)
                os.chmod(binary_name, 0o755)
                print("Yuklash muvaffaqiyatli!")
            except Exception as e:
                print("Yuklashda xatolik:", e)
                sys.exit(1)

        cmd = f"./{binary_name}"
        print("Tunnel ishga tushirilmoqda (Port 8080)...")
        lt_proc = subprocess.Popen(
            [cmd, "tunnel", "--url", "http://localhost:8080"], 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            text=True, encoding='utf-8', errors='replace'
        )

        url = None
        start_time = time.time()
        for line in iter(lt_proc.stdout.readline, ''):
            print("CF:", line.strip())
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if match:
                url = match.group(0)
                break
            if time.time() - start_time > 30:
                break

        if not url:
            print("Cloudflare Tunnel ishga tushmadi!")
            lt_proc.kill()
            exit(1)
            
        def read_cf_output():
            for l in iter(lt_proc.stdout.readline, ''):
                pass
        threading.Thread(target=read_cf_output, daemon=True).start()

print(f"Muvaffaqiyatli URL: {url}")

config_path = os.path.join(SCRIPT_DIR, "config.py")
print(f"config.py yangilanmoqda... ({config_path})")
with open(config_path, "r", encoding="utf-8") as f:
    content = f.read()

new_content = re.sub(r'WEBAPP_URL\s*=\s*".*?"', f'WEBAPP_URL = "{url}"', content)
with open(config_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Telegram Bot ishga tushirilmoqda...")
bot_proc = subprocess.Popen(
    ["python", os.path.join(SCRIPT_DIR, "main.py")], 
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
    text=True, encoding='utf-8', errors='replace',
    cwd=SCRIPT_DIR
)

def print_bot_output():
    for line in iter(bot_proc.stdout.readline, ''):
        print("BOT:", line.strip())

threading.Thread(target=print_bot_output, daemon=True).start()

try:
    bot_proc.wait()
except KeyboardInterrupt:
    pass
finally:
    try: lt_proc.kill()
    except: pass
    try: bot_proc.kill()
    except: pass
    print("Barcha jarayonlar to'xtatildi.")
