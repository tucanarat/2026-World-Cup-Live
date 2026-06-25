import os
import requests
from datetime import datetime, timedelta

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")

standings_url = "https://api.football-data.org/v4/competitions/WC/standings"
matches_url = "https://api.football-data.org/v4/competitions/WC/matches"
headers = {"X-Auth-Token": API_KEY} if API_KEY else {}

# API'den gelebilecek tüm olası varyasyonları kapsayan büyük harf indeksli Türkçe sözlük
TR_TEAMS = {
    # A Grubu
    "MEXICO": "Meksika", "SOUTH AFRICA": "Güney Afrika", "SOUTH KOREA": "Güney Kore", "KOREA REPUBLIC": "Güney Kore", "REP. KOREA": "Güney Kore", "CZECHIA": "Çekya", "CZECH REPUBLIC": "Çekya",
    # B Grubu
    "CANADA": "Kanada", "BOSNIA AND HERZEGOVINA": "Bosna-Hersek", "BOSNIA-HERZEGOVINA": "Bosna-Hersek", "BOSNIA": "Bosna-Hersek", "QATAR": "Katar", "SWITZERLAND": "İsviçre",
    # C Grubu
    "BRAZIL": "Brezilya", "MOROCCO": "Fas", "HAITI": "Haiti", "SCOTLAND": "İskoçya",
    # D Grubu
    "USA": "ABD", "UNITED STATES": "ABD", "UNITED STATES OF AMERICA": "ABD", "PARAGUAY": "Paraguay", "AUSTRALIA": "Avustralya", "TURKEY": "Türkiye", "TÜRKIYE": "Türkiye",
    # E Grubu
    "GERMANY": "Almanya", "CURAÇAO": "Curaçao", "CURACAO": "Curaçao", "IVORY COAST": "Fildişi Sahili", "CÔTE D'IVOIRE": "Fildişi Sahili", "COTE D'IVOIRE": "Fildişi Sahili", "ECUADOR": "Ekvador",
    # F Grubu
    "NETHERLANDS": "Hollanda", "JAPAN": "Japonya", "SWEDEN": "İsveç", "TUNISIA": "Tunus",
    # G Grubu
    "BELGIUM": "Belçika", "EGYPT": "Mısır", "IRAN": "İran", "IR IRAN": "İran", "ISLAMIC REPUBLIC OF IRAN": "İran", "NEW ZEALAND": "Yeni Zelanda",
    # H Grubu
    "SPAIN": "İspanya", "CAPE VERDE": "Yeşil Burun Adaları", "CABO VERDE": "Yeşil Burun Adaları", "CAPE VERDE ISLANDS": "Yeşil Burun Adaları", "SAUDI ARABIA": "Suudi Arabistan", "URUGUAY": "Uruguay",
    # I Grubu
    "FRANCE": "Fransa", "SENEGAL": "Senegal", "IRAQ": "Irak", "NORWAY": "Norveç",
    # J Grubu
    "ARGENTINA": "Arjantin", "ALGERIA": "Cezayir", "AUSTRIA": "Avusturya", "JORDAN": "Ürdün",
    # K Grubu
    "PORTUGAL": "Portekiz", "DR CONGO": "Demokratik Kongo Cumhuriyeti", "CONGO DR": "Demokratik Kongo Cumhuriyeti", "DEMOCRATIC REPUBLIC OF THE CONGO": "Demokratik Kongo Cumhuriyeti", "CONGO DEMOCRATIC REPUBLIC": "Demokratik Kongo Cumhuriyeti", "UZBEKISTAN": "Özbekistan", "COLOMBIA": "Kolombiya",
    # L Grubu
    "ENGLAND": "İngiltere", "CROATIA": "Hırvatistan", "GHANA": "Gana", "PANAMA": "Panama"
}

def translate(name):
    if not name: 
        return "Bekliyor..."
    
    # Gelen ismi temizleyip büyük harfe çeviriyoruz (böylece eşleşme ihtimali kesinleşiyor)
    name_str = str(name).strip().upper()
    
    # Sözlükte varsa Türkçe karşılığını, yoksa API'den gelen orijinal ismi (ilk harfleri büyük formatta) döndürür
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
        .status-qualified { font-weight: 600; color: #0f172a; background-color: #f0fdf4; }
        .status-eliminated { color: #cbd5e1 !important; opacity: 0.55; }
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
        for index, row in enumerate(group.get("table", [])):
            team_obj = row.get("team") or {}
            t_name = translate(team_obj.get("name"))
            t_flag = team_obj.get("crest", "")
            played = row.get("playedGames", 0)
            points = row.get("points", 0)
            gd = row.get("goalDifference", 0)
            row_style = ""
            if played == 3:
                if index < 2: row_style = ' class="status-qualified"'
                elif index > 2: row_style = ' class="status-eliminated"'
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
                a_cls = 'class="winner"' if winner == "AWAY_TEAM" else ('class="loser"' if winner == "HOME_TEAM" else "")
                html_content += f'<div class="match-card"><div class="m-teams"><div class="m-line {h_cls}">{h_flag_html}<span>{h_name}</span></div><div class="m-line {a_cls}">{a_flag_html}<span>{a_name}</span></div></div><div class="m-scores"><div>{h_score if h_score is not None else "-"}</div><div>{a_score if a_score is not None else "-"}</div></div></div>'

if not has_bracket:
    html_content += "<p style='text-align:center;font-size:12px;color:#64748b;padding:20px;'>Grup aşaması tamamlandıktan sonra turnuva ağacı aktif olacaktır.</p>"

html_content += '</div></div><div id="fixtures" class="tab-content"><div class="matches-list">'
today_matches, other_matches = [], []

if all_matches:
    for m in all_matches:
        if not m: continue
        if (m.get("utcDate") or "")[:10] == current_date_str: today_matches.append(m)
        else: other_matches.append(m)

if today_matches:
    html_content += '<div class="section-divider">Bugünün Maçları</div>'
    for m in today_matches:
        h_obj = m.get("homeTeam") or {}
        a_obj = m.get("awayTeam") or {}
        h_name, a_name = translate(h_obj.get("name")), translate(a_obj.get("name"))
        h_flag_html = f'<img src="{h_obj.get("crest")}" class="flag">' if h_obj.get("crest") else '<span class="tbd-icon">🏆</span>'
        a_flag_html = f'<img src="{a_obj.get("crest")}" class="flag">' if a_obj.get("crest") else '<span class="tbd-icon">🏆</span>'
        full_time = (m.get("score") or {}).get("fullTime") or {}
        h_score, a_score = full_time.get("home"), full_time.get("away")
        status = m.get("status")
        badge = '<span class="status-badge badge-live">CANLI</span>' if status == "IN_PLAY" else ('<span class="status-badge badge-end">BİTTİ</span>' if status == "FINISHED" else f'<span class="status-badge badge-time">{parse_tsi_time(m.get("utcDate"))} TSİ</span>')
        html_content += f'<div class="match-card today"><div class="m-teams"><div class="m-line">{h_flag_html}<span>{h_name}</span></div><div class="m-line">{a_flag_html}<span>{a_name}</span></div></div><div class="m-scores"><div>{h_score if h_score is not None else "-"}</div><div>{a_score if a_score is not None else "-"}</div></div><div class="m-info">{badge}</div></div>'

if other_matches:
    html_content += '<div class="section-divider">Tüm Karşılaşmalar</div>'
    for m in other_matches[:50]:
        h_obj = m.get("homeTeam") or {}
        a_obj = m.get("awayTeam") or {}
        h_name, a_name = translate(h_obj.get("name")), translate(a_obj.get("name"))
        h_flag_html = f'<img src="{h_obj.get("crest")}" class="flag">' if h_obj.get("crest") else '<span class="tbd-icon">🏆</span>'
        a_flag_html = f'<img src="{a_obj.get("crest")}" class="flag">' if a_obj.get("crest") else '<span class="tbd-icon">🏆</span>'
        full_time = (m.get("score") or {}).get("fullTime") or {}
        h_score, a_score = full_time.get("home"), full_time.get("away")
        status = m.get("status")
        badge = '<span class="status-badge badge-end">BİTTİ</span>' if status == "FINISHED" else f'<span class="status-badge badge-time">{parse_tsi_time(m.get("utcDate"))} TSİ</span>'
        html_content += f'<div class="match-card"><div class="m-teams"><div class="m-line">{h_flag_html}<span>{h_name}</span></div><div class="m-line">{a_flag_html}<span>{a_name}</span></div></div><div class="m-scores"><div>{h_score if h_score is not None else "-"}</div><div>{a_score if a_score is not None else "-"}</div></div><div class="m-info">{badge}</div></div>'

html_content += """</div></div>
<script>
    function openTab(tabId) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        if(event && event.currentTarget) { event.currentTarget.classList.add('active'); }
    }
</script></body></html>"""

with open("wc2026_groups_live.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("HTML dosyası başarıyla üretildi.")
