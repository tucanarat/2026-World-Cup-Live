import os
import requests

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
if not API_KEY:
    print("HATA: API Anahtarı bulunamadı!")
    exit(1)

url = "https://api.football-data.org/v4/competitions/WC/standings"
headers = {"X-Auth-Token": API_KEY}

try:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"API Hatası: {response.status_code}")
        exit(1)
        
    data = response.json()
    standings = data.get("standings", [])
    
    html_content = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>2026 FIFA Dünya Kupası Canlı Puan Durumu</title>
    <style>
        body { font-family: sans-serif; background: #f5f5f5; padding: 20px; color: #333; }
        .group-card { background: white; margin-bottom: 20px; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h2 { color: #8a2463; border-bottom: 2px solid #8a2463; padding-bottom: 5px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 8px; text-align: center; border-bottom: 1px solid #ddd; }
        th { background: #fafafa; }
    </style>
</head>
<body>
    <h1>2026 FIFA Dünya Kupası - Canlı Puan Durumu</h1>
"""

    for group in standings:
        group_name = group.get("group", "Grup")
        html_content += f'<div class="group-card"><h2>{group_name}</h2>'
        html_content += "<table><tr><th>Takım</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AG</th><th>YG</th><th>AV</th><th>P</th></tr>"
        
        for table_row in group.get("table", []):
            team_name = table_row.get("team", {}).get("name", "Bilinmeyen Takım")
            played = table_row.get("playedGames", 0)
            won = table_row.get("won", 0)
            draw = table_row.get("draw", 0)
            lost = table_row.get("lost", 0)
            gf = table_row.get("goalsFor", 0)
            ga = table_row.get("goalsAgainst", 0)
            gd = table_row.get("goalDifference", 0)
            points = table_row.get("points", 0)
            
            html_content += f"<tr><td>{team_name}</td><td>{played}</td><td>{won}</td><td>{draw}</td><td>{lost}</td><td>{gf}</td><td>{ga}</td><td>{gd}</td><td>{points}</td></tr>"
            
        html_content += "</table></div>"
        
    html_content += "</body></html>"
    
    with open("wc2026_groups_live.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("HTML başarıyla güncellendi.")

except Exception as e:
    print(f"Bir hata oluştu: {e}")
