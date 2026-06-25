import os
import requests
import subprocess
from datetime import datetime

# API Ayarları
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")
standings_url = "https://api.football-data.org/v4/competitions/WC/standings"
headers = {"X-Auth-Token": API_KEY} if API_KEY else {}

# ... (TR_TEAMS sözlüğü ve translate fonksiyonu aynı kalacak) ...

# HTML'i üreten ana kısım
def generate_html():
    # ... (Buraya yukarıdaki turnuva ağacı ve puan durumu kodlarını koyun) ...
    return html_content

# HTML'i oluştur ve dosyaya yaz
html = generate_html()
with open("wc2026_groups_live.html", "w", encoding="utf-8") as f:
    f.write(html)

# SİSTEMİ GÜNCELLEMEK İÇİN GİT KOMUTLARI
try:
    subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "github-actions@github.com"], check=True)
    subprocess.run(["git", "add", "wc2026_groups_live.html"], check=True)
    
    # Değişiklik varsa commit at ve push yap
    status = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
    if status.returncode != 0:
        subprocess.run(["git", "commit", "-m", "Güncelleme: Turnuva ağacı ve veri yapısı"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Değişiklikler başarıyla sunucuya gönderildi.")
    else:
        print("Dosyada bir değişiklik yok.")
except Exception as e:
    print(f"Git hatası: {e}")
