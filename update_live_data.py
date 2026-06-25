import os
import requests
from datetime import datetime, timedelta

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")

standings_url = "https://api.football-data.org/v4/competitions/WC/standings"
matches_url = "https://api.football-data.org/v4/competitions/WC/matches"
headers = {"X-Auth-Token": API_KEY} if API_KEY else {}

TR_TEAMS = {
    "MEXICO": "Meksika", "SOUTH AFRICA": "Güney Afrika", "SOUTH KOREA": "Güney Kore", "KOREA REPUBLIC": "Güney Kore", "REP. KOREA": "Güney Kore", "CZECHIA": "Çekya", "CZECH REPUBLIC": "Çekya",
    "CANADA": "Kanada", "BOSNIA AND HERZEGOVINA": "Bosna-Hersek", "BOSNIA-HERZEGOVINA": "Bosna-Hersek", "BOSNIA": "Bosna-Hersek", "QATAR": "Katar", "SWITZERLAND": "İsviçre",
    "BRAZIL": "Brezilya", "MOROCCO": "Fas", "HAITI": "Haiti", "SCOTLAND": "İskoçya",
    "USA": "ABD", "UNITED STATES": "ABD", "UNITED STATES OF AMERICA": "ABD", "PARAGUAY": "Paraguay", "AUSTRALIA": "Avustralya", "TURKEY": "Türkiye", "TÜRKIYE": "Türkiye",
    "GERMANY": "Almanya", "CURAÇAO": "Curaçao", "CURACAO": "Curaçao", "IVORY COAST": "Fildişi Sahili", "CÔTE D'IVOIRE": "Fildişi Sahili", "COTE D'IVOIRE": "Fildişi Sahili", "ECUADOR": "Ekvador",
    "NETHERLANDS": "Hollanda", "JAPAN": "Japonya", "SWEDEN": "İsveç", "TUNISIA": "Tunus",
    "BELGIUM": "Belçika", "EGYPT": "Mısır", "IRAN": "İran", "IR IRAN": "İran", "ISLAMIC REPUBLIC OF IRAN": "İran", "NEW ZEALAND": "Yeni Zelanda",
    "SPAIN": "İspanya", "CAPE VERDE": "Yeşil Burun Adaları", "CABO VERDE": "Yeşil Burun Adaları", "CAPE VERDE ISLANDS": "Yeşil Burun Adaları", "SAUDI ARABIA": "Suudi Arabistan", "URUGUAY": "Uruguay",
    "FRANCE": "Fransa", "SENEGAL": "Senegal", "IRAQ": "Irak", "NORWAY": "Norveç",
    "ARGENTINA": "Arjantin", "ALGERIA": "Cezayir", "AUSTRIA": "Avusturya", "JORDAN": "Ürdün",
    "PORTUGAL": "Portekiz", "DR CONGO": "Demokratik Kongo Cumhuriyeti", "CONGO DR": "Demokratik Kongo Cumhuriyeti", "DEMOCRATIC REPUBLIC OF THE CONGO": "Demokratik Kongo Cumhuriyeti", "CONGO DEMOCRATIC REPUBLIC": "Demokratik Kongo Cumhuriyeti", "UZBEKISTAN": "Özbekistan", "COLOMBIA": "Kolombiya",
    "ENGLAND": "İngiltere", "CROATIA": "Hırvatistan", "GHANA": "Gana", "PANAMA": "Panama"
}

def translate(name):
    if not name: return "Bekliyor..."
    name_str = str(name).strip().upper()
    return TR_TEAMS.get(name_str, str(name).strip())

def parse_tsi_time(utc_date_str):
    if not utc_date_str: return "--:--"
    try:
        utc_dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
        return (utc_dt + timedelta(hours=3)).strftime("%H:%M")
    except: return "--:--"

standings = []
all_matches = []

if API_KEY:
    try:
        r = requests.get(standings_url, headers=headers, timeout=15)
        if r.status_code == 200: standings = r.json().get("standings", [])
    except: pass
    try:
        r = requests.get(matches_url, headers=headers, timeout=15)
        if r.status_code == 200: all_matches = r.json().get("matches", [])
    except: pass

current_date_str = datetime.utcnow().strftime("%Y-%m-%d")

html_content = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 Dünya Kupası Canlı Takip</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background: #ffffff; margin: 0; padding: 5px; color: #111111; -webkit-font-smoothing: antialiased; }
        html, body { overflow-x: hidden; }
        ::-webkit-scrollbar { display: none !important; }
        .header-container { text-align: center; padding: 12px 0; border-bottom: 1px solid #f3f4f6; margin-bottom: 15px; }
        .header-container h1 { font-size: 18px; font-weight: 700; margin: 0; letter-spacing: -0.5px; color: #0f172a; }
        .header-container p { font-size: 10px; color: #10b981; font-weight: 600; margin: 3px 0 0 0; text-transform: uppercase; letter-spacing: 0.5px; }
        .tabs { display: flex; justify-content: center; margin-bottom: 15px; gap: 4px; border-bottom: 1px solid #f1f5f9; }
        .tab-btn { background: none; border: none; color: #64748b; padding: 10px 14px; cursor: pointer; font-size: 13px; font-weight: 500; border-bottom: 2px solid transparent; }
        .tab-btn.active { color: #10b981; font-weight: 600; border-bottom: 2px solid #10b981; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .groups-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; padding: 2px; }
        .group-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px; }
        .group-title { font-size: 12px; font-weight: 700; color: #0f172a; margin: 0 0 8px 0; padding-bottom: 5px; border-bottom: 1px solid #f1f5f9; text-transform: uppercase; }
        table { width: 100%; border-collapse: collapse; font-size: 12px; }
        th, td { padding: 5px 3px; text-align: center; }
        th { color: #94a3b8; font-weight: 600; font-size: 10px; }
        td { border-bottom: 1px solid #f8fafc; color: #334155; }
        .team-cell { display: flex; align-items: center; gap: 6px; text-align: left; font-weight: 500; }
        .flag { width: 16px; height: 11px; object-fit: cover; border: 1px solid #e2e8f0; }
        .tbd-icon { font-size: 11px; color: #94a3b8; }
        .status-qualified { font-weight: 600; color: #16a34a; background-color: #f0fdf4; }
        .status-eliminated { color: #94a3b8 !important; opacity: 0.45; background-color: #f8fafc; }
        .matches-list, .bracket-container { display: flex; flex-direction: column; gap: 6px; max-width: 480px; margin: 0 auto; padding: 2px; }
        .section-divider { font-size: 10px; font-weight: 700; color: #64748b; margin: 12px 0 4px 0; text-transform: uppercase; display: flex; align-items: center; gap: 6px; }
        .section-divider::after { content: ''; flex: 1; height: 1px; background: #f1f5f9; }
        .match-card { display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 5px; font-size: 12px; }
        .match-card.today { border-color: #10b981; background: #f0fdf4; }
        .m-teams { display: flex; flex-direction: column; gap: 5px; flex: 1; }
        .m-line { display: flex; align-items: center; gap: 6px; }
        .m-scores { display: flex; flex-direction: column; gap: 5px; font-weight: 700; text-align: right; width: 20px; color: #0f172a; }
        .m-info { display: flex; flex-direction: column; align-items: flex-end; justify-content: center; padding-left: 8px; border-left: 1px solid #f1f5f9; margin-left: 8px; min-width: 55px; }
        .status-badge { font-size: 9px; font-weight: 700; padding: 1px 4px; border-radius: 2px; text-transform: uppercase; }
        .badge-live { background: #ef4444; color: #ffffff; animation: pulse 1.5s infinite; }
        .badge-time { background: #f1f5f9; color: #475569; }
        .badge-end { background: #f8fafc; color: #94a3b8; border: 1px solid #e2e8f0; }
        .winner { font-weight: 600; color: #0f172a; }
        .loser { color: #cbd5e1; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <div class="header-container"><h1>2026 FIFA DÜNYA KUPASI</h1><p>Canlı Turnuva Merkezi</p></div>
    <div class="tabs">
        <button class="tab-btn active" onclick="openTab('groups')">⚽ Puan Durumu</button>
        <button class="tab-btn" onclick="openTab('bracket')">🌿 Turnuva Ağacı</button>
        <button class="tab-btn" onclick="openTab('fixtures')">📅 Karşılaşmalar</button>
    </div>
    <div id="groups" class="tab-content active"><div class="groups-grid">
"""

if standings:
    for group in standings:
        g_name = group.get("group", "Grup").replace("GROUP_", "Grup ")
        html_content += f'<div class="group-card"><h2 class="group-title">{g_name}</h2>'
        html_content += "<table><tr><th style='text-align:left;'>Takım</th><th>O</th><th>AV</th><th>P</th></tr>"
        
        table_rows = group.get("table", [])
        
        # Grubun tüm puan verilerini güvenli bir listeye alalım
        group_points = []
        for r in table_rows:
            p_val = r.get("points")
            group_points.append(int(p_val) if p_val is not None else 0)
        
        for index, row in enumerate(table_rows):
            team_obj = row.get("team") or {}
            t_name = translate(team_obj.get("name"))
            t_flag = team_obj.get("crest", "")
            
            p_games = row.get("playedGames")
            p_pts = row.get("points")
            p_gd = row.get("goalDifference")
            
            played = int(p_games) if p_games is not None else 0
            points = int(p_pts) if p_pts is not None else 0
            gd = int(p_gd) if p_gd is not None else 0
            
            row_style = ""
            
            # Durum 1: Grup aşaması bu takım için bittiyse (3 Maç)
            if played == 3:
                if index < 2: 
                    row_style = ' class="status-qualified"'
                elif index == 3: 
                    row_style = ' class="status-eliminated"'
            
            # Durum 2: Takım henüz 2 maç oynamış ama matematiksel olarak elenmişse
            elif played == 2:
                # Maksimum ulaşabileceği puan
                max_possible = points + 3
                # Grupta bu puandan kesinlikle daha yüksek puana sahip olan takım sayısı
                higher_teams = sum(1 for p in group_points if p > max_possible)
                
                # Eğer 3 takım birden bu puanı geçmişse, takım hiçbir koşulda 4. sıradan kurtulamaz -> Elendi
                if higher_teams >= 3:
                    row_style = ' class="status-eliminated"'
                # Özel İstisna: 0 puanlı sonuncu takımlar için diğer ikilinin 4+ puanı varsa (Örn: Türkiye'nin grubu)
                elif points == 0 and len(group_points) == 4:
                    # Gruptaki diğer takımların puan sıralamasına bakarak 3. olma ihtimalini tamamen yitirdiyse
                    sorted_points = sorted(group_points, reverse=True)
                    if sorted_points[2] >= 4:
                        row_style = ' class="status-eliminated"'

            flag_html = f'<img src="{t_flag}" class="flag">' if t_flag else '<span class="tbd-icon">🏆</span>'
            html_content += f"<tr{row_style}><td class='team-cell'>{flag_html}<span>{t_name}</span></td><td>{played}</td><td>{gd}</td><td>{points}</td></tr>"
        html_content += "</table></div>"
else:
    html_content += "<p style='text-align:center;font-size:12px;color:#64748b;grid-column:1/-1;padding:20px;'>Puan durumu verisi yükleniyor...</p>"

html_content += '</div></div><div id="bracket" class="tab-content"><div class="bracket-container">'
stages = {"LAST_32": "Son 32 Turu", "LAST_16": "Son 16 Turu", "QUARTER_FINALS": "Çeyrek Final", "SEMI_FINALS": "Yarı Final", "FINAL": "Final"}
has_bracket = False

if all_matches:
    for stage_key, stage_title in stages.items():
        stage_matches = [m for m in all_matches if m and m.get("stage") == stage_key]
        if stage_matches:
            has_bracket = True
            html_content += f'<div class="section-divider">{stage_title}</div>'
            for m in stage_matches:
                home_obj = m.get("homeTeam") or {}
                away_obj = m.get("awayTeam") or {}
                h_name = translate(home_obj.get("name")) if home_obj.get("name") else "Üst Tur Takımı"
                a_name = translate(away_obj.get("name")) if away_obj.get("name") else "Üst Tur Takımı"
                h_flag = home_obj.get("crest") if home_obj else ""
                a_flag = away_obj.get("crest") if away_obj else ""
                h_flag_html = f'<img src="{h_flag}" class="flag">' if h_flag else '<span class="tbd-icon">🏆</span>'
                a_flag_html = f'<img src="{a_flag}" class="flag">' if a_flag else '<span class="tbd-icon">🏆</span>'
                score_obj = m.get("score") or {}
                full_time = score_obj.get("fullTime") or {}
                h_score = full_time.get("home")
                a_score = full_time.get("away")
                winner = score_obj.get("winner")
                h_cls = 'class="winner"' if winner == "HOME_TEAM" else ('class="loser"' if winner == "AWAY_TEAM" else "")
                a_cls
