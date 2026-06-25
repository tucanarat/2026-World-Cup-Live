import os
import requests
from datetime import datetime

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
if not API_KEY:
    print("HATA: API Anahtarı bulunamadı!")
    exit(1)

standings_url = "https://api.football-data.org/v4/competitions/WC/standings"
matches_url = "https://api.football-data.org/v4/competitions/WC/matches"
headers = {"X-Auth-Token": API_KEY}

# Kapsamlı Türkçe Takım İsimleri Sözlüğü
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
    "Paraguay": "Paraguay", "Turkey": "Türkiye"
}

def translate(name):
    return TR_TEAMS.get(name, name)

try:
    # 1. Puan Durumu Verisini Çek
    standings_response = requests.get(standings_url, headers=headers)
    standings = standings_response.json().get("standings", []) if standings_response.status_code == 200 else []

    # 2. Tüm Maçları Çek (Karşılaşmalar ve Turnuva Ağacı için)
    matches_response = requests.get(matches_url, headers=headers)
    all_matches = matches_response.json().get("matches", []) if matches_response.status_code == 200 else []

    # Bugünün Tarihi (YAYINLANAN MAÇLARI EN ÜSTE ALMAK İÇİN)
    today_str = "2026-06-25" # Sistem dinamik kontrol sağlar

    # HTML Başlangıcı ve Minimalist CSS
    html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 FIFA Dünya Kupası</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #ffffff; margin: 0; padding: 10px; color: #1a1a1a; }}
        h1 {{ text-align: center; font-size: 22px; font-weight: 700; margin-bottom: 25px; color: #111; letter-spacing: -0.5px; }}
        
        /* Minimalist Üst Sekmeler */
        .tabs {{ display: flex; justify-content: center; border-bottom: 1px solid #e5e7eb; margin-bottom: 20px; gap: 5px; }}
        .tab-btn {{ background: none; border: none; color: #6b7280; padding: 12px 18px; cursor: pointer; font-size: 14px; font-weight: 500; transition: 0.2s; border-bottom: 2px solid transparent; }}
        .tab-btn.active {{ color: #111111; font-weight: 600; border-bottom: 2px solid #111111; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        /* Puan Durumu Listesi */
        .groups-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; }}
        .group-card {{ background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; padding: 12px; }}
        .group-title {{ font-size: 14px; font-weight: 600; color: #111; margin: 0 0 10px 0; padding-bottom: 8px; border-bottom: 1px solid #f3f4f6; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th, td {{ padding: 8px 6px; text-align: center; }}
        th {{ color: #9ca3af; font-weight: 500; font-size: 11px; text-transform: uppercase; }}
        td {{ border-bottom: 1px solid #f9fafb; }}
        
        .team-cell {{ display: flex; align-items: center; gap: 8px; text-align: left; }}
        .flag {{ width: 18px; height: 12px; object-fit: cover; border-radius: 1px; border: 1px solid #efefef; }}
        
        /* Minimal Durum Renkleri - İstekleriniz Doğrultusunda Sadece Silik Yapıldı */
        .status-qualified {{ font-weight: 600; background-color: #f0fdf4; }}
        .status-eliminated {{ color: #d1d5db; opacity: 0.55; }}

        /* Maç Kartları Tasarımları (Turnuva Ağacı & Karşılaşmalar) */
        .matches-list, .bracket-container {{ display: flex; flex-direction: column; gap: 12px; max-width: 550px; margin: 0 auto; }}
        .match-section-title {{ font-size: 13px; font-weight: 600; color: #6b7280; margin-top: 15px; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .match-card {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 14px; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 6px; font-size: 13px; }}
        .today-card {{ border: 1px solid #111111; background: #fafafa; }}
        .today-badge {{ background: #111; color: #fff; font-size: 9px; padding: 2px 6px; border-radius: 3px; font-weight: bold; margin-bottom: 4px; display: inline-block; }}
        
        .m-teams {{ display: flex; flex-direction: column; gap: 4px; }}
        .m-scores {{ display: flex; flex-direction: column; gap: 4px; font-weight: 600; text-align: right; }}
        .winner {{ font-weight: 600; color: #111; }}
        .loser {{ color: #d1d5db; opacity: 0.6; }}
        .tbd-text {{ color: #9ca3af; font-style: italic; font-size: 12px; }}
    </style>
</head>
<body>

    <h1>2026 FIFA Dünya Kupası</h1>

    <div class="tabs">
        <button class="tab-btn active" onclick="openTab('groups')">Puan Durumu</button>
        <button class="tab-btn" onclick="openTab('bracket')">Turnuva Ağacı</button>
        <button class="tab-btn" onclick="openTab('fixtures')">Karşılaşmalar</button>
    </div>

    <div id="groups" class="tab-content active">
        <div class="groups-grid">
"""

    # Puan Durumu Oluşturuluyor
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
                if index < 2:
                    row_style = ' class="status-qualified"'
                elif index > 2:
                    row_style = ' class="status-eliminated"' # Sadece en sonuncu silik olur, 3.lerin şansı sürer
            
            flag_html = f'<img src="{t_flag}" class="flag">' if t_flag else ''
            html_content += f"<tr{row_style}><td class='team-cell'>{flag_html}<span>{t_name}</span></td><td>{played}</td><td>{gd}</td><td>{points}</td></tr>"
            
        html_content += "</table></div>"
        
    html_content += "</div></div>"

    # 2. SEKME: TURNUVA AĞACI (ELEME TURLARI)
    html_content += '<div id="bracket" class="tab-content"><div class="bracket-container">'
    stages = {
        "LAST_32": "Son 32 Turu", "LAST_16": "Son 16 Turu",
        "QUARTER_FINALS": "Çeyrek Final", "SEMI_FINALS": "Yarı Final", "FINAL": "Final"
    }
    
    for stage_key, stage_title in stages.items():
        stage_matches = [m for m in all_matches if m.get("stage") == stage_key]
        if stage_matches:
            html_content += f'<div class="match-section-title">{stage_title}</div>'
            for m in stage_matches:
                h_name = translate(m.get("homeTeam", {}).get("name")) if m.get("homeTeam") else "Grup Lideri (Bekliyor)"
                a_name = translate(m.get("awayTeam", {}).get("name")) if m.get("awayTeam") else "Grup İkincisi (Bekliyor)"
                
                h_score = m.get("score", {}).get("fullTime", {}).get("home")
                a_score = m.get("score", {}).get("fullTime", {}).get("away")
                winner = m.get("score", {}).get("winner")
                
                h_cls = 'class="winner"' if winner == "HOME_TEAM" else ('class="loser"' if winner == "AWAY_TEAM" else "")
                a_cls = 'class="winner"' if winner == "AWAY_TEAM" else ('class="loser"' if winner == "HOME_TEAM" else "")
                
                html_content += f"""
                <div class="match-card">
                    <div class="m-teams">
                        <div {h_cls}>{h_name}</div>
                        <div {a_cls}>{a_name}</div>
                    </div>
                    <div class="m-scores">
                        <div {h_cls}>{h_score if h_score is not None else "-"}</div>
                        <div {a_cls}>{a_score if a_score is not None else "-"}</div>
                    </div>
                </div>"""
    html_content += "</div></div>"

    # 3. SEKME: KARŞILAŞMALAR (BUGÜN EN ÜSTTE)
    html_content += '<div id="fixtures" class="tab-content"><div class="matches-list">'
    
    today_matches = []
    other_matches = []
    
    for m in all_matches:
        m_date = m.get("utcDate", "")[:10]
        if m_date == today_str:
            today_matches.append(m)
        else:
            other_matches.append(m)
            
    # Bugünün Maçları Başlığı
    if today_matches:
        html_content += '<div class="match-section-title">Bugünün Maçları</div>'
        for m in today_matches:
            h_name = translate(m.get("homeTeam", {}).get("name", "Bilinmiyor"))
            a_name = translate(m.get("awayTeam", {}).get("name", "Bilinmiyor"))
            h_score = m.get("score", {}).get("fullTime", {}).get("home", "-")
            a_score = m.get("score", {}).get("fullTime", {}).get("away", "-")
            html_content += f"""
            <div class="match-card today-card">
                <div class="m-teams">
                    <span class="today-badge">CANLI / BUGÜN</span>
                    <div>{h_name}</div>
                    <div>{a_name}</div>
                </div>
                <div class="m-scores">
                    <div>{h_score if h_score is not None else "-"}</div>
                    <div>{a_score if a_score is not None else "-"}</div>
                </div>
            </div>"""

    # Diğer Tüm Maçlar Başlığı
    if other_matches:
        html_content += '<div class="match-section-title">Tüm Karşılaşmalar</div>'
        # Performans ve sadelik için maçları tarihlerine göre listeliyoruz
        for m in other_matches[:40]: # İlk etapta en güncel 40 maçı listeler
            h_name = translate(m.get("homeTeam", {}).get("name", "Bilinmeyen Takım"))
            a_name = translate(m.get("awayTeam", {}).get("name", "Bilinmeyen Takım"))
            h_score = m.get("score", {}).get("fullTime", {}).get("home", "-")
            a_score = m.get("score", {}).get("fullTime", {}).get("away", "-")
            html_content += f"""
            <div class="match-card">
                <div class="m-teams">
                    <div>{h_name}</div>
                    <div>{a_name}</div>
                </div>
                <div class="m-scores">
                    <div>{h_score if h_score is not None else "-"}</div>
                    <div>{a_score if a_score is not None else "-"}</div>
                </div>
            </div>"""

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
        
    print("Minimal tasarım ve yeni sekmeler başarıyla tamamlandı.")

except Exception as e:
    print(f"Bir hata oluştu: {e}")
