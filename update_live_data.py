import os
import requests
from datetime import datetime, timedelta

# GitHub Actions üzerinden gelen gizli anahtarı okur
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

if not API_KEY:
    print("HATA: API Anahtarı bulunamadı!")
    exit(1)

standings_url = "https://api.football-data.org/v4/competitions/WC/standings"
matches_url = "https://api.football-data.org/v4/competitions/WC/matches"
headers = {"X-Auth-Token": API_KEY}

# Türkçe sözlük
TR_TEAMS = {
    "MEXICO": "Meksika", "SOUTH AFRICA": "Güney Afrika", "SOUTH KOREA": "Güney Kore", 
    "KOREA REPUBLIC": "Güney Kore", "REP. KOREA": "Güney Kore", "CANADA": "Kanada", 
    "USA": "ABD", "UNITED STATES": "ABD", "TURKEY": "Türkiye", "TÜRKIYE": "Türkiye", 
    "GERMANY": "Almanya", "NETHERLANDS": "Hollanda", "JAPAN": "Japonya", 
    "BELGIUM": "Belçika", "SPAIN": "İspanya", "FRANCE": "Fransa", "ARGENTINA": "Arjantin", 
    "PORTUGAL": "Portekiz", "ENGLAND": "İngiltere", "CROATIA": "Hırvatistan", 
    "BRAZIL": "Brezilya", "MOROCCO": "Fas", "ECUADOR": "Ekvador", "TUNISIA": "Tunus", 
    "IRAN": "İran", "GHANA": "Gana", "PANAMA": "Panama", "URUGUAY": "Uruguay", 
    "COLOMBIA": "Kolombiya", "SWITZERLAND": "İsviçre", "DENMARK": "Danimarka", 
    "SERBIA": "Sırbistan", "POLAND": "Polonya", "AUSTRALIA": "Avustralya", 
    "SAUDI ARABIA": "Suudi Arabistan", "CZECHIA": "Çekya", "QATAR": "Katar", 
    "SCOTLAND": "İskoçya", "SWEDEN": "İsveç", "EGYPT": "Mısır", "NORWAY": "Norveç", 
    "AUSTRIA": "Avusturya", "ALGERIA": "Cezayir", "JORDAN": "Ürdün", 
    "UZBEKISTAN": "Özbekistan", "ITALY": "İtalya", "SENEGAL": "Senegal",
    "WALES": "Galler", "COSTA RICA": "Kosta Rika", "CAMEROON": "Kamerun",
    "PARAGUAY": "Paraguay", "PERU": "Peru", "CHILE": "Şili", "UKRAINE": "Ukrayna", "NIGERIA": "Nijerya"
}

def translate(name):
    if not name: return "Bekliyor..."
    return TR_TEAMS.get(str(name).strip().upper(), str(name))

def parse_tsi_time(utc_date_str):
    if not utc_date_str: return "--:--"
    try:
        utc_dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
        tsi_dt = utc_dt + timedelta(hours=3)
        return tsi_dt.strftime("%H:%M")
    except:
        return "--:--"

# Verileri çek
try:
    standings = requests.get(standings_url, headers=headers, timeout=10).json().get("standings", [])
    all_matches = requests.get(matches_url, headers=headers, timeout=10).json().get("matches", [])
except Exception as e:
    print(f"Hata: {e}")
    exit(1)

# Basit bir HTML oluştur
html_content = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dünya Kupası</title></head><body>"
html_content += "<h1>Puan Durumu</h1>"

for group in standings:
    g_name = group.get("group", "Grup").replace("GROUP_", "Grup ")
    html_content += f"<h2>{g_name}</h2><table border='1'><tr><th>Takım</th><th>P</th></tr>"
    for row in group.get("table", []):
        t_name = translate(row.get("team", {}).get("name"))
        pts = row.get("points")
        html_content += f"<tr><td>{t_name}</td><td>{pts}</td></tr>"
    html_content += "</table>"

html_content += "</body></html>"

# Dosyayı kaydet
with open("wc2026_groups_live.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML dosyası başarıyla güncellendi.")
