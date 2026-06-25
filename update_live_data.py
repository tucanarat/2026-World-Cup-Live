import os
import requests
from datetime import datetime, timedelta

# API anahtarı yoksa hata verip çökmek yerine boş string atayıp devam etmesini sağlıyoruz
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")

standings_url = "https://api.football-data.org/v4/competitions/WC/standings"
matches_url = "https://api.football-data.org/v4/competitions/WC/matches"
headers = {"X-Auth-Token": API_KEY} if API_KEY else {}

# 2026 Dünya Kupası'ndaki Kesin 48 Takım ve API Varyasyonları Sözlüğü
TR_TEAMS = {
    # A Grubu
    "Mexico": "Meksika", "South Africa": "Güney Afrika", "South Korea": "Güney Kore", "Korea Republic": "Güney Kore", "Czechia": "Çekya", "Czech Republic": "Çekya",
    # B Grubu
    "Canada": "Kanada", "Bosnia and Herzegovina": "Bosna-Hersek", "Bosnia-Herzegovina": "Bosna-Hersek", "Qatar": "Katar", "Switzerland": "İsviçre",
    # C Grubu
    "Brazil": "Brezilya", "Morocco": "Fas", "Haiti": "Haiti", "Scotland": "İskoçya",
    # D Grubu
    "USA": "ABD", "United States": "ABD", "United States of America": "ABD", "Paraguay": "Paraguay", "Australia": "Avustralya", "Turkey": "Türkiye", "Türkiye": "Türkiye",
    # E Grubu
    "Germany": "Almanya", "Curaçao": "Curaçao", "Curacao": "Curaçao", "Ivory Coast": "Fildişi Sahili", "Cote d'Ivoire": "Fildişi Sahili", "Ecuador": "Ekvador",
    # F Grubu
    "Netherlands": "Hollanda", "Japan": "Japonya", "Sweden": "İsveç", "Tunisia": "Tunus",
    # G Grubu
    "Belgium": "Belçika", "Egypt": "Mısır", "Iran": "İran", "IR Iran": "İran", "New Zealand": "Yeni Zelanda",
    # H Grubu
    "Spain": "İspanya", "Cape Verde": "Yeşil Burun Adaları", "Cabo Verde": "Yeşil Burun Adaları", "Saudi Arabia": "Suudi Arabistan", "Uruguay": "Uruguay",
    # I Grubu
    "France": "Fransa", "Senegal": "Senegal", "Iraq": "Irak", "Norway": "Norveç",
    # J Grubu
    "Argentina": "Arjantin", "Algeria": "Cezayir", "Austria": "Avusturya", "Jordan": "Ürdün",
    # K Grubu
    "Portugal": "Portekiz", "DR Congo": "Demokratik Kongo Cumhuriyeti", "Congo DR": "Demokratik Kongo Cumhuriyeti", "Democratic Republic of the Congo": "Demokratik Kongo Cumhuriyeti", "Uzbekistan": "Özbekistan", "Colombia": "Kolombiya",
    # L Grubu
    "England": "İngiltere", "Croatia": "Hırvatistan", "Ghana": "Gana", "Panama": "Panama"
}

def translate(name):
    if not name: 
        return "Bekliyor..."
    name_str = str(name).strip()
    return TR_TEAMS.get(name_str, name_str)

def parse_tsi_time(utc_date_str):
    if not utc_date_str: return "--:--"
    try:
        utc_dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
        tsi_dt = utc_dt + timedelta(hours=3)
        return tsi_dt.strftime("%H:%M")
    except:
        return "--:--"

try:
    standings = []
    if API_KEY:
        try:
            r = requests.get(standings_url, headers=headers, timeout=15)
            if r.status_code == 200: standings = r.json().get("standings", [])
        except Exception as e:
            print(f"Puan durumu çekilemedi: {e}")

    all_matches = []
    if API_KEY:
        try:
            r = requests.get(matches_url, headers=headers, timeout=15)
            if r.status_code == 200: all_matches = r.json().get("matches", [])
        except Exception as e:
            print(f"Maçlar çekilemedi: {e}")

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
        .tab-btn { background: none; border: none; color: #64748b; padding: 10px 14px; cursor: pointer; font-size: 13px; font-weight: 500; display: flex; align-items: center; gap: 6px; transition: all 0.15s; border-bottom: 2px solid transparent; }
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
        .flag { width: 16px; height: 11px; object-fit: cover; border-radius: 1px; border: 1px solid #e2e8f0; }
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
        .m-scores { display: flex; flex-direction: column; gap
