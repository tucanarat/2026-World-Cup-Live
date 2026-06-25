import os
import requests
from datetime import datetime, timedelta

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
if not API_KEY:
    print("HATA: API Anahtarı bulunamadı!")
    exit(1)

standings_url = "https://api.football-data.org/v4/competitions/WC/standings"
matches_url = "https://api.football-data.org/v4/competitions/WC/matches"
headers = {"X-Auth-Token": API_KEY}

# Eksiksiz Türkçe Dünya Kupası Takım Sözlüğü
TR_TEAMS = {
    "Argentina": "Arjantin", "Brazil": "Brezilya", "France": "Fransa", "Germany": "Almanya",
    "Spain": "İspanya", "England": "İngiltere", "Italy": "İtalya", "Netherlands": "Hollanda",
    "Portugal": "Portekiz", "Belgium": "Belçika", "Croatia": "Hırvatistan", "Uruguay": "Uruguay",
    "Mexico": "Meksika", "United States": "ABD", "Canada": "Kanada", "Morocco": "Fas",
    "Japan": "Japonya", "South Korea": "Güney Kore", "Australia": "Avustralya", "Senegal": "Senegal",
    "Iran": "İran", "Saudi Arabia": "Suudi Arabistan", "Qatar": "Katar", "Ecuador": "Ekvador",
    "Wales": "Galler", "Poland": "Polonya", "Tunisia": "Tunus", "Denmark": "Danimarka",
    "Costa Rica": "Kosta Rika", "Switzerland": "İsviçre", "Cameroon": "Kamerun", "Ghana": "Gana",
    "Czechia": "Çekya", "Bosnia-Herzegovina": "Bosna Hersek", "Scotland": "İskoçya", "Haiti": "Haiti",
    "Paraguay": "Paraguay", "Turkey": "Türkiye", "Peru": "Peru", "Colombia": "Kolombiya",
    "Chile": "Şili", "Sweden": "İsveç", "Norway": "Norveç", "Ukraine": "Ukrayna", 
    "Serbia": "Sırbistan", "Algeria": "Cezayir", "Egypt": "Mısır", "Nigeria": "Nijerya"
}

def translate(name):
    if not name: return "Bekliyor..."
    return TR_TEAMS.get(name, name)

def parse_tsi_time(utc_date_str):
    try:
        utc_dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
        tsi_dt = utc_dt + timedelta(hours=3)
        return tsi_dt.strftime("%H:%M")
    except:
        return "--:--"

try:
    standings_response = requests.get(standings_url, headers=headers)
    standings = standings_response.json().get("standings", []) if standings_response.status_code == 200 else []

    matches_response = requests.get(matches_url, headers=headers)
    all_matches = matches_response.json().get("matches", []) if matches_response.status_code == 200 else []

    current_date_str = datetime.utcnow().strftime("%Y-%m-%d")

    html_content = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 Dünya Kupası Canlı Takip</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background: #ffffff; margin: 0; padding: 5px; color: #111111; -webkit-font-smoothing: antialiased; overflow-x: hidden; }
        ::-webkit-scrollbar { display: none; }
        
        .header-container { text-align: center; padding: 15px 0; border-bottom: 1px solid #f0f0f0; margin-bottom: 15px; }
        .header-container h1 { font-size: 20px; font-weight: 700; margin: 0; letter-spacing: -0.5px; color: #0f172a; }
        .header-container p { font-size: 11px; color: #10b981; font-weight: 600; margin: 4px 0 0 0; text-transform: uppercase; letter-spacing: 1px; }

        .tabs { display: flex; justify-content: center; margin-bottom: 20px; gap: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 1px; }
        .tab-btn { background: none; border: none; color: #64748b; padding: 10px 16px; cursor: pointer; font-size: 13px; font-weight: 500; display: flex; align-items: center; gap: 6px; transition: all 0.2s; border-bottom: 2px solid transparent; }
        .tab-btn.active { color: #10b981; font-weight: 600; border-bottom: 2px solid #10b981; }

        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .groups-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 16px; padding: 5px; }
        .group-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; }
        .group-title { font-size: 13px; font-weight: 700; color: #0f172a; margin: 0 0 10px 0; padding-bottom: 6px; border-bottom: 1px solid #f1f5f9; text-transform: uppercase; }
        
        table { width: 100%; border-collapse: collapse; font-size: 12px; }
        th, td { padding: 6px 4px; text-align: center; }
        th { color: #94a3b8; font-weight: 600; font-size: 10px; text-transform: uppercase; }
        td { border-bottom: 1px solid #f8fafc; color: #334155; }
        
        .team-cell { display: flex; align-items: center; gap: 8px; text-align: left; font-weight: 500; }
        .flag { width: 16px; height: 11px; object-fit: cover; border-radius: 1px; border: 1px solid #e2e8f0; }
        .tbd-icon { font-size: 12px; color: #94a3b8; }

        .status-qualified { font-weight: 600; color: #0f172a; background-color: #f0fdf4; }
        .status-eliminated { color: #cbd5e1 !important; opacity: 0.6; }

        .matches-list, .bracket-container { display: flex; flex-direction: column; gap: 8px; max-width: 500px; margin: 0 auto; padding: 5px; }
        .section-divider { font-size: 11px; font-weight: 700; color: #64748b; margin: 15px 0 6px 0; text-transform: uppercase; display: flex; align-items: center; gap: 8px; }
        .section-divider::after { content: ''; flex: 1; height: 1px; background: #f1f5f9; }
        
        .match-card { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 12px; }
        .match-card.today { border-color: #10b981; background: #f0fdf4; }
        
        .m-teams { display: flex; flex-direction: column; gap: 6px; flex: 1; }
        .m-line { display: flex; align-items: center; gap: 8px; }
        .m-scores { display: flex; flex-direction: column; gap: 6px; font-weight: 700; text-align: right; width: 25px; color: #0f172a; }
        
        .m-info { display: flex; flex-direction: column; align-items: flex-end; justify-content: center; padding-left: 10px; border-left: 1px solid #f1f5f9; margin-left: 10px; min-width: 60px; }
        .status-badge { font-size: 9px; font-weight: 700; padding: 2px 5px; border-radius: 3px; text-transform: uppercase; }
        .badge-live { background: #ef4444; color: #ffffff; animation: pulse 1.5s infinite; }
        .badge-time { background: #f1f5f9; color: #475569; }
        .badge-end { background: #f8fafc; color: #94a3b8; border: 1px solid #e2e8f0; }

        .winner { font-weight: 600; color: #0f172a; }
        .loser { color: #cbd5e1; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>

    <div class="header-container">
        <h1>2026 FIFA DÜNYA KUPASI</h1>
        <p>Canlı Turnuva Merkezi</p>
    </div>

    <div class="tabs">
        <button class="tab-btn active" onclick="openTab('groups')">⚽ Puan Durumu</button>
        <button class="tab-btn" onclick="openTab('bracket')">🌿 Turnuva Ağacı</button>
        <button class="tab-btn" onclick="openTab('fixtures')">📅 Karşılaşmalar</button>
    </div>

    <div id="groups" class="tab-content active">
        <div class="groups-grid">
"""

    for group in standings:
        g_name = group.get("group", "Grup").replace("GROUP_", "Grup ")
        html_content += f'<div class="group-card"><h2 class="group-title">{g_name}</h2>'
        html_content += "<table><tr><th style='text-align:left;'>Takım</th><th>O</th><th>AV</th><th>P</th></tr>"
        
        for index, row in enumerate(group.get("table", [])):
            t_name = translate(row.get("team", {}).get("name", ""))
            t_flag = row.get("team", {}).get("crest", "")
            played = row.get("playedGames", 0)
            points = row.get("points", 0)
            gd = row.get("goalDifference", 0)
            
            row_style = ""
            if played == 3:
                if index < 2
