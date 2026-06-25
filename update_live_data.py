import os
import requests

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")
headers = {"X-Auth-Token": API_KEY} if API_KEY else {}

TR_TEAMS = {
    "MEXICO": "Meksika", "SOUTH AFRICA": "Güney Afrika", "SOUTH KOREA": "Güney Kore", "CANADA": "Kanada",
    "USA": "ABD", "TURKEY": "Türkiye", "GERMANY": "Almanya", "NETHERLANDS": "Hollanda", "JAPAN": "Japonya",
    "BELGIUM": "Belçika", "SPAIN": "İspanya", "FRANCE": "Fransa", "ARGENTINA": "Arjantin", "PORTUGAL": "Portekiz",
    "ENGLAND": "İngiltere", "CROATIA": "Hırvatistan", "BRAZIL": "Brezilya", "MOROCCO": "Fas", "ECUADOR": "Ekvador",
    "TUNISIA": "Tunus", "IRAN": "İran", "GHANA": "Gana", "PANAMA": "Panama", "URUGUAY": "Uruguay", "COLOMBIA": "Kolombiya"
}

def translate(name):
    return TR_TEAMS.get(str(name).strip().upper(), str(name).strip())

def get_standings():
    try:
        r = requests.get("https://api.football-data.org/v4/competitions/WC/standings", headers=headers, timeout=10)
        return r.json().get("standings", []) if r.status_code == 200 else []
    except: return []

html = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dünya Kupası Puan Durumu</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 10px; background-color: #f8fafc; color: #334; }
        .group { margin-bottom: 20px; background: white; padding: 12px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        h2 { color: #0f172a; font-size: 15px; margin: 0 0 10px 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 5px; }
        table { width: 100%; border-collapse: collapse; }
        th { font-size: 11px; color: #94a3b8; padding: 5px; }
        td { padding: 8px 5px; text-align: center; border-bottom: 1px solid #f1f5f9; font-size: 13px; }
        .team-cell { display: flex; align-items: center; gap: 8px; text-align: left; }
        .flag { width: 20px; height: 14px; object-fit: cover; border-radius: 2px; }
    </style>
</head>
<body>
    <h1 style="text-align:center; font-size: 20px;">Dünya Kupası 2026</h1>
"""

for group in get_standings():
    html += f'<div class="group"><h2>{group.get("group").replace("GROUP_", "Grup ")}</h2><table>'
    html += '<tr><th style="text-align:left;">Takım</th><th>O</th><th>P</th></tr>'
    for row in group.get("table", []):
        team_obj = row.get("team", {})
        name = translate(team_obj.get("name"))
        flag = team_obj.get("crest", "")
        played = row.get("playedGames", 0)
        points = row.get("points", 0)
        
        html += f'''<tr>
            <td class="team-cell">
                <img src="{flag}" class="flag" onerror="this.style.display='none'">
                {name}
            </td>
            <td>{played}</td>
            <td style="font-weight:bold;">{points}</td>
        </tr>'''
    html += '</table></div>'

html += "</body></html>"

with open("wc2026_groups_live.html", "w", encoding="utf-8") as f:
    f.write(html)
