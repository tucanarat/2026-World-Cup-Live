import os
import requests

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")
headers = {"X-Auth-Token": API_KEY} if API_KEY else {}

def get_standings():
    try:
        r = requests.get("https://api.football-data.org/v4/competitions/WC/standings", headers=headers, timeout=10)
        return r.json().get("standings", []) if r.status_code == 200 else []
    except: return []

html = """<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8"><title>Puan Durumu</title>
<style>
    body { font-family: sans-serif; padding: 20px; color: #333; }
    .group { margin-bottom: 30px; border: 1px solid #eee; padding: 15px; border-radius: 8px; }
    h2 { color: #10b981; font-size: 18px; margin-top: 0; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 8px; text-align: center; border-bottom: 1px solid #f9f9f9; }
</style></head><body><h1>Puan Durumu</h1>"""

for group in get_standings():
    html += f'<div class="group"><h2>{group.get("group").replace("GROUP_", "Grup ")}</h2><table>'
    html += '<tr><th>Takım</th><th>O</th><th>P</th></tr>'
    for row in group.get("table", []):
        team = row.get("team", {}).get("name", "Takım")
        played = row.get("playedGames", 0)
        points = row.get("points", 0)
        html += f'<tr><td>{team}</td><td>{played}</td><td>{points}</td></tr>'
    html += '</table></div>'

html += "</body></html>"

with open("wc2026_groups_live.html", "w", encoding="utf-8") as f:
    f.write(html)
