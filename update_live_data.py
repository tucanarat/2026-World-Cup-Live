import os
import requests

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
if not API_KEY:
    print("HATA: API Anahtarı bulunamadı!")
    exit(1)

standings_url = "https://api.football-data.org/v4/competitions/WC/standings"
matches_url = "https://api.football-data.org/v4/competitions/WC/matches?stage=LAST_32,LAST_16,QUARTER_FINALS,SEMI_FINALS,FINAL"
headers = {"X-Auth-Token": API_KEY}

try:
    # 1. Puan Durumu Verisini Çek
    standings_response = requests.get(standings_url, headers=headers)
    if standings_response.status_code != 200:
        print("Puan durumu çekilemedi")
        exit(1)
    standings_data = standings_response.json()
    standings = standings_data.get("standings", [])

    # HTML Tasarımı
    html_content = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 FIFA Dünya Kupası</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; margin: 0; padding: 15px; color: #2c3e50; }
        h1 { text-align: center; color: #8a2463; font-size: 24px; margin-bottom: 20px; }
        
        /* Sekme Sistemi */
        .tabs { display: flex; justify-content: center; margin-bottom: 20px; gap: 10px; }
        .tab-btn { background: #fff; border: 2px solid #8a2463; color: #8a2463; padding: 10px 20px; cursor: pointer; font-weight: bold; border-radius: 20px; transition: 0.3s; }
        .tab-btn.active, .tab-btn:hover { background: #8a2463; color: #fff; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        /* Grup Kartları */
        .groups-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }
        .group-card { background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); overflow: hidden; }
        .group-title { background: #8a2463; color: white; padding: 12px; margin: 0; font-size: 16px; text-align: center; }
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        th, td { padding: 10px 8px; text-align: center; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; font-weight: 600; color: #7f8c8d; }
        
        /* Takım Hücresi ve Bayrak */
        .team-cell { display: flex; align-items: center; gap: 8px; text-align: left; }
        .flag { width: 20px; height: 14px; object-fit: cover; border-radius: 2px; border: 1px solid #ddd; }
        
        /* Renk Skalası */
        .legend { display: flex; justify-content: center; gap: 15px; margin-bottom: 15px; font-size: 12px; font-weight: bold; }
        .leg-item { display: flex; align-items: center; gap: 5px; }
        
        /* Grup Aşaması Durum Stilleri */
        .status-qualified { background-color: rgba(46, 204, 113, 0.12) !important; font-weight: bold; }
        .status-qualified .team-name::after { content: " ✔"; color: #2ecc71; font-size: 11px; }
        
        .status-eliminated { background-color: rgba(231, 76, 60, 0.03) !important; color: #bdc3c7; opacity: 0.6; }
        .status-active { background-color: #ffffff; }

        /* Turnuva Ağacı */
        .bracket-container { display: flex; flex-direction: column; align-items: center; gap: 20px; padding: 20px 0; }
        .bracket-round { width: 100%; max-width: 600px; background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .bracket-round h3 { margin-top: 0; color: #8a2463; border-bottom: 2px solid #f4f6f9; padding-bottom: 5px; }
        .matchup { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; background: #f8f9fa; margin-bottom: 8px; border-radius: 6px; border-left: 4px solid #8a2463; }
        .match-teams { display: flex; flex-direction: column; gap: 6px; }
        .match-scores { display: flex; flex-direction: column; gap: 6px; font-weight: bold; text-align: right; }
        
        /* Stiller */
        .winner { font-weight: bold; color: #2c3e50; }
        .loser { color: #bdc3c7; opacity: 0.5; }
        .tbd-team { color: #e67e22; font-style: italic; font-size: 13px; }
    </style>
</head>
<body>

    <h1>2026 FIFA Dünya Kupası</h1>

    <div class="tabs">
        <button class="tab-btn active" onclick="openTab('groups')">Puan Durumu</button>
        <button class="tab-btn" onclick="openTab('bracket')">Turnuva Ağacı</button>
    </div>

    <!-- 1. SEKME: PUAN DURUMU -->
    <div id="groups" class="tab-content active">
        <div class="legend">
            <div class="leg-item"><span style="background:rgba(46,204,113,0.15); width:15px; height:15px; border-radius:3px; display:inline-block;"></span> Üst Tur Garantilendi</div>
            <div class="leg-item"><span style="background:#fff; border:1px solid #ddd; width:15px; height:15px; border-radius:3px; display:inline-block;"></span> İddiası Sürüyor / En İyi 3.lük İhtimali</div>
            <div class="leg-item"><span style="background:rgba(231,76,60,0.05); width:15px; height:15px; border-radius:3px; display:inline-block;"></span> Elendi (Silik)</div>
        </div>

        <div class="groups-grid">
"""

    for group in standings:
        group_name = group.get("group", "Grup")
        html_content += f'<div class="group-card"><h2 class="group-title">{group_name}</h2>'
        html_content += "<table><tr><th style='text-align:left;'>Takım</th><th>O</th><th>G</th><th>B</th><th>M</th><th>AV</th><th>P</th></tr>"
        
        table_rows = group.get("table", [])
        
        for index, table_row in enumerate(table_rows):
            team_data = table_row.get("team", {})
            team_name = team_data.get("name", "Bilinmeyen Takım")
            flag_url = team_data.get("crest", "")
            
            played = table_row.get("playedGames", 0)
            points = table_row.get("points", 0)
            gd = table_row.get("goalDifference", 0)
            
            if played == 3:
                if index < 2:
                    row_style = ' class="status-qualified"'
                elif index == 2:
                    row_style = ' class="status-active"'
                else:
                    row_style = ' class="status-eliminated"'
            else:
                if points >= 6:
                    row_style = ' class="status-qualified"'
                elif played == 2 and points == 0 and gd <= -4:
                    row_style = ' class="status-eliminated"'
                else:
                    row_style = ' class="status-active"'
            
            flag_img = f'<img src="{flag_url}" class="flag" alt=""> ' if flag_url else ''
            html_content += f"<tr{row_style}><td class='team-cell'>{flag_img}<span class='team-name'>{team_name}</span></td><td>{played}</td><td>{table_row.get('won',0)}</td><td>{table_row.get('draw',0)}</td><td>{table_row.get('lost',0)}</td><td>{gd}</td><td>{points}</td></tr>"
            
        html_content += "</table></div>"
        
    html_content += "</div></div>"

    # 2. SEKME: TURNUVA AĞACI
    html_content += '<div id="bracket" class="tab-content"><div class="bracket-container">'
    
    # 2. Maç Verilerini Çek
    matches_response = requests.get(matches_url, headers=headers)
    stages = {
        "LAST_32": "Son 32 Turu",
        "LAST_16": "Son 16 Turu",
        "QUARTER_FINALS": "Çeyrek Final",
        "SEMI_FINALS": "Yarı Final",
        "FINAL": "Final"
    }
    
    if matches_response.status_code == 200:
        matches_data = matches_response.json().get("matches", [])
        
        for stage_key, stage_title in stages.items():
            stage_matches = [m for m in matches_data if m.get("stage") == stage_key]
            if stage_matches:
                html_content += f'<div class="bracket-round"><h3>{stage_title}</h3>'
                for match in stage_matches:
                    home_team_obj = match.get("homeTeam")
                    away_team_obj = match.get("awayTeam")
                    
                    home_team = home_team_obj.get("name") if (home_team_obj and home_team_obj.get("name")) else None
                    away_team = away_team_obj.get("name") if (away_team_obj and away_team_obj.get("name")) else None
                    
                    # Hata veren string kontrolü düzeltildi: Google tarzı yer tutucular daha esnek hale getirildi
                    home_is_tbd = False
                    away_is_tbd = False
                    
                    if not home_team:
                        home_team = "Üst Tur Takımı (Bekliyor)"
                        home_is_tbd = True
                    if not away_team:
                        away_team = "Üst Tur Takımı (Bekliyor)"
                        away_is_tbd = True

                    home_score = match.get("score", {}).get("fullTime", {}).get("home")
                    away_score = match.get("score", {}).get("fullTime", {}).get("away")
                    winner_code = match.get("score", {}).get("winner")
                    
                    home_class = 'class="tbd-team"' if home_is_tbd else ""
                    away_class = 'class="tbd-team"' if away_is_tbd else ""
                    
                    if winner_code == "HOME_TEAM":
                        home_class = 'class="winner"'
                        away_class = 'class="loser"'
                    elif winner_code == "AWAY_TEAM":
                        home_class = 'class="loser"'
                        away_class = 'class="winner"'
                    
                    display_home_score = home_score if home_score is not None else "-"
                    display_away_score = away_score if away_score is not None else "-"
                    
                    html_content += f"""
                    <div class="matchup">
                        <div class="match-teams">
                            <div {home_class}>{home_team}</div>
                            <div {away_class}>{away_team}</div>
                        </div>
                        <div class="match-scores">
                            <div {home_class}>{display_home_score}</div>
                            <div {away_class}>{display_away_score}</div>
                        </div>
                    </div>
                    """
                html_content += "</div>"
    else:
        html_content += "<p>Turnuva ağacı verisi şu an güncellenemiyor.</p>"

    html_content += """
    </div></div>
    <script>
        function openTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }
    </script>
</body>
</html>
"""
    
    with open("wc2026_groups_live.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("Sistem başarıyla stabilize edildi.")

except Exception as e:
    print(f"Bir hata oluştu: {e}")
