import os
import requests
from datetime import datetime, timedelta

# API Ayarları
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")
matches_url = "https://api.football-data.org/v4/competitions/WC/matches"
headers = {"X-Auth-Token": API_KEY} if API_KEY else {}

# Türkçe isim sözlüğü
TR_TEAMS = {
    "MEXICO": "Meksika", "SOUTH KOREA": "Güney Kore", "CANADA": "Kanada", "BRAZIL": "Brezilya", "MOROCCO": "Fas",
    "USA": "ABD", "PARAGUAY": "Paraguay", "AUSTRALIA": "Avustralya", "TURKEY": "Türkiye", "GERMANY": "Almanya",
    "NETHERLANDS": "Hollanda", "JAPAN": "Japonya", "BELGIUM": "Belçika", "SPAIN": "İspanya", "FRANCE": "Fransa",
    "ARGENTINA": "Arjantin", "PORTUGAL": "Portekiz", "ENGLAND": "İngiltere", "CROATIA": "Hırvatistan"
}

def translate(name):
    if not name: return "TBD"
    return TR_TEAMS.get(str(name).strip().upper(), str(name).strip())

def get_bracket_section():
    # 2026 Dünya Kupası resmi eleme ağacı yapısı (Slotlar)
    bracket_structure = [
        ("Son 32", ["Maç 1 (G1 - En İyi 3.)", "Maç 2 (G2 - En İyi 3.)", "Maç 3 (G3 - G4)", "Maç 4 (G5 - G6)", 
                    "Maç 5 (G7 - G8)", "Maç 6 (G9 - G10)", "Maç 7 (G11 - G12)", "Maç 8 (Diğer Eşleşmeler)"]),
        ("Son 16", ["Çeyrek Final Yolu A", "Çeyrek Final Yolu B", "Çeyrek Final Yolu C", "Çeyrek Final Yolu D"]),
        ("Çeyrek Final", ["Yarı Final A", "Yarı Final B"]),
        ("Yarı Final", ["Final Yolu"]),
        ("FİNAL", ["ŞAMPİYONLUK MAÇI"])
    ]
    
    html = '<div class="bracket-container">'
    for stage, matches in bracket_structure:
        html += f'<div class="section-divider">🏆 {stage}</div>'
        for match in matches:
            html += f'''
            <div class="match-card">
                <div class="m-teams" style="width: 100%; text-align: center; font-size: 11px; color: #64748b;">
                    {match}
                </div>
            </div>'''
    html += '</div>'
    return html

# HTML içeriğini oluştururken 'bracket' sekmesini bu fonksiyonla çağırın:
# <div id="bracket" class="tab-content">
#    {get_bracket_section()}
# </div>
