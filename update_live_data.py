import os
import requests
from datetime import datetime, timedelta

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")
standings_url = "https://api.football-data.org/v4/competitions/WC/standings"
matches_url = "https://api.football-data.org/v4/competitions/WC/matches"
headers = {"X-Auth-Token": API_KEY} if API_KEY else {}

TR_TEAMS = {
    "MEXICO": "Meksika", "SOUTH AFRICA": "Güney Afrika", "SOUTH KOREA": "Güney Kore", "CANADA": "Kanada",
    "USA": "ABD", "TURKEY": "Türkiye", "GERMANY": "Almanya", "NETHERLANDS": "Hollanda", "JAPAN": "Japonya",
    "BELGIUM": "Belçika", "SPAIN": "İspanya", "FRANCE": "Fransa", "ARGENTINA": "Arjantin", "PORTUGAL": "Portekiz",
    "ENGLAND": "İngiltere", "CROATIA": "Hırvatistan", "BRAZIL": "Brezilya", "MOROCCO": "Fas"
}

def translate(name):
    return TR_TEAMS.get(str(name).strip().upper(), str(name).strip())

def get_bracket_section():
    # 2026 Dünya Kupası resmi eşleşme yolu (Slotlar)
    html = '<div class="bracket-container">'
    html += '<div class="section-divider">🏆 SON 32 EŞLEŞME YOLU</div>'
    slots = [
        ("Grup A 1.si", "Grup B 2.si", "Maç 1"), ("Grup B 1.si", "Grup C 2.si", "Maç 2"),
        ("Grup C 1.si", "Grup D 2.si", "Maç 3"), ("Grup D 1.si", "Grup E 2.si", "Maç 4"),
        ("Grup E 1.si", "Grup F 2.si", "Maç 5"), ("Grup F 1.si", "Grup G 2.si", "Maç 6"),
        ("Grup G 1.si", "Grup H 2.si", "Maç 7"), ("Grup H 1.si", "Grup A 2.si", "Maç 8")
    ]
    for t1, t2, mid in slots:
        html += f'<div class="match-card"><div class="m-teams" style="width:100%; display:flex; justify-content:space-between; font-size:11px;"><span>{t1}</span><span style="color:#10b981;">vs</span><span>{t2}</span></div><div style="font-size:9px; color:#94a3b8; text-align:center; margin-top:5px;">{mid}</div></div>'
    html += '</div>'
    return html

# Veri çekme ve HTML oluşturma
standings = []
try:
    r = requests.get(standings_url, headers=headers, timeout=10)
    if r.status_code == 200: standings = r.json().get("standings", [])
except: pass

html_content = """<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8"><style>
    body { font-family: sans-serif; padding: 10px; }
    .tabs { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; }
    .tab-content { display: none; }
    .tab-content.active { display: block; }
    .group-card { border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; }
    .status-eliminated { opacity: 0.4; }
    .section-divider { font-weight: bold; margin: 15px 0; color: #10b981; }
    .match-card { border: 1px solid #eee; padding: 8px; margin-bottom: 5px; }
</style></head><body>
<div class="tabs">
    <button onclick="openTab('groups')">⚽ Puan Durumu</button>
    <button onclick="openTab('bracket')">🏆 Turnuva Ağacı</button>
</div>
<div id="groups" class="tab-content active">"""

for group in standings:
    html_content += f'<div class="group-card"><h3>{group.get("group").replace("GROUP_", "Grup ")}</h3><table>'
    for row in group.get("table", []):
        played = int(row.get("playedGames") or 0)
        points = int(row.get("points") or 0)
        style = ' class="status-eliminated"' if (played == 2 and points == 0) else ""
        html_content += f'<tr{style}><td>{translate(row["team"]["name"])}</td><td>{points}P</td></tr>'
    html_content += '</table></div>'

html_content += f'</div><div id="bracket" class="tab-content">{get_bracket_section()}</div>'
html_content += """<script>
    function openTab(id) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.getElementById(id).classList.add('active');
    }
</script></body></html>"""

with open("wc2026_groups_live.html", "w", encoding="utf-8") as f:
    f.write(html_content)
