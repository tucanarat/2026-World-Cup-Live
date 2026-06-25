import os
import requests

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")
headers = {"X-Auth-Token": API_KEY} if API_KEY else {}

def get_standings():
    try:
        r = requests.get("https://api.football-data.org/v4/competitions/WC/standings", headers=headers, timeout=10)
        return r.json().get("standings", []) if r.status_code == 200 else []
    except: return []

# HTML İçeriği (Mobil uyumlu ve minimalist)
html = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dünya Kupası Puan Durumu</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 10px; color: #333; margin: 0; background-color: #f4f4f9; }
        .group { margin-bottom: 20px; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h1 { text-align: center; font-size: 20px; color: #1a1a1a; }
        h2 { color: #10b981; font-size: 16px; margin-top: 0; border-bottom: 2px solid #10b981; display: inline-block; padding-bottom: 5px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th { color: #666; font-size: 12px; text-transform: uppercase; }
        th, td { padding: 10px 5px; text-align: center; border-bottom: 1px solid #eee; }
        td:first-child { text-align: left; font-weight: 500; }
    </style>
</head>
<body>
    <h1>FIFA 2026 Puan Durumu</h1>
"""

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
