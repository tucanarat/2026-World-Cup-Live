import os
import requests

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")
headers = {"X-Auth-Token": API_KEY} if API_KEY else {}

# İSİM EŞLEŞTİRME SÖZLÜĞÜ (Genişletildi)
TR_TEAMS = {
    "MEXICO": "Meksika", "SOUTH AFRICA": "Güney Afrika", "SOUTH KOREA": "Güney Kore", 
    "KOREA REPUBLIC": "Güney Kore", "REP. KOREA": "Güney Kore", "CANADA": "Kanada", 
    "USA": "ABD", "UNITED STATES": "ABD", "TURKEY": "Türkiye", "TÜRKIYE": "Türkiye", 
    "GERMANY": "Almanya", "NETHERLANDS": "Hollanda", "JAPAN": "Japonya", 
    "BELGIUM": "Belçika", "SPAIN": "İspanya", "FRANCE": "Fransa", "ARGENTINA": "Arjantin", 
    "PORTUGAL": "Portekiz", "ENGLAND": "İngiltere", "CROATIA": "Hırvatistan", 
    "BRAZIL": "Brezilya", "MOROCCO": "Fas", "ECUADOR": "Ekvador", "TUNISIA": "Tunus", 
    "IRAN": "İran", "IR IRAN": "İran", "GHANA": "Gana", "PANAMA": "Panama", 
    "URUGUAY": "Uruguay", "COLOMBIA": "Kolombiya", "SWITZERLAND": "İsviçre", 
    "DENMARK": "Danimarka", "SERBIA": "Sırbistan", "POLAND": "Polonya", 
    "AUSTRALIA": "Avustralya", "SAUDI ARABIA": "Suudi Arabistan"
}

def translate(name):
    # İsimleri temizle ve sözlükte ara
    clean_name = str(name).strip().upper()
    return TR_TEAMS.get(clean_name, str(name).strip())

def get_standings():
    try:
        r = requests.get("https://api.football-data.org/v4/competitions/WC/standings", headers=headers, timeout=10)
        return r.json().get("standings", []) if r.status_code == 200 else []
    except: return []

html = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f4f4; padding: 20px; }
        .group-card { background: white; margin-bottom: 20px; padding: 15px; border-radius: 10px; border-top: 5px solid #2ecc71; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { color: #2c3e50; margin-top: 0; font-size: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th { background: #f8f9fa; padding: 10px; text-align: center; color: #7f8c8d; }
        td { padding: 12px; text-align: center; border-bottom: 1px solid #eee; }
        .team-info { display: flex; align-items: center; gap: 10px; justify-content: start; }
        .flag { width: 30px; height: 20px; object-fit: cover; border-radius: 3px; box-shadow: 0 0 2px rgba(0,0,0,0.2); }
    </style>
</head>
<body>
    <h1 style="text-align:center;">2026 Dünya Kupası Puan Durumu</h1>
"""

for group in get_standings():
    group_name = group.get("group", "").replace("GROUP_", "Grup ")
    html += f'<div class="group-card"><h2>{group_name}</h2><table>'
    html += '<tr><th style="text-align:left;">Takım</th><th>O</th><th>P</th></tr>'
    for row in group.get("table", []):
        team_obj = row.get("team", {})
        original_name = team_obj.get("name", "Bilinmiyor")
        name = translate(original_name)
        flag = team_obj.get("crest", "")
        played = row.get("playedGames", 0)
        points = row.get("points", 0)
        html += f'<tr><td class="team-info"><img src="{flag}" class="flag" onerror="this.style.display=\'none\'">{name}</td><td>{played}</td><td style="font-weight:bold;">{points}</td></tr>'
    html += '</table></div>'

html += "</body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
