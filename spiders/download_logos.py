# -*- coding: utf-8 -*-
"""Logo Downloader for Onde Vai Passar Futebol Hoje"""

import os
import json
import requests
from pathlib import Path
import time

# Base directories
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / 'assets'
TIMES_DIR = ASSETS_DIR / 'times'
CAMPEONATOS_DIR = ASSETS_DIR / 'campeonatos'
CANAIS_DIR = ASSETS_DIR / 'canais'
DATA_DIR = BASE_DIR / 'data'

# Create directories
for directory in [TIMES_DIR, CAMPEONATOS_DIR, CANAIS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Team logo URLs mapping (team_id -> logo_url)
TEAMS_LOGOS = {
    'saopaulo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg/150px-Brasao_do_Sao_Paulo_Futebol_Clube.svg.png',
    'corinthians': 'https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/Sport_Club_Corinthians_Paulista_crest.svg/150px-Sport_Club_Corinthians_Paulista_crest.svg.png',
    'palmeiras': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Palmeiras_logo.svg/150px-Palmeiras_logo.svg.png',
    'santos': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Santos_Logo.png/150px-Santos_Logo.png',
    'bragantino': 'https://upload.wikimedia.org/wikipedia/en/thumb/0/07/Red_Bull_Bragantino_logo.svg/150px-Red_Bull_Bragantino_logo.svg.png',
    'pontepreta': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/AA_Ponte_Preta.svg/150px-AA_Ponte_Preta.svg.png',
    'guarani': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Guarani_FC.svg/150px-Guarani_FC.svg.png',
    'botafogorp': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Botafogo_Futebol_Clube_%28Ribeir%C3%A3o_Preto%29.svg/150px-Botafogo_Futebol_Clube_%28Ribeir%C3%A3o_Preto%29.svg.png',
    'mirassol': 'https://upload.wikimedia.org/wikipedia/pt/thumb/9/91/Mirassol_Futebol_Clube.png/150px-Mirassol_Futebol_Clube.png',
    'novorizontino': 'https://upload.wikimedia.org/wikipedia/pt/thumb/5/5b/Novorizontino.png/150px-Novorizontino.png',
    'saobernardofc': 'https://upload.wikimedia.org/wikipedia/pt/thumb/4/42/S%C3%A3o_Bernardo_Futebol_Clube.png/150px-S%C3%A3o_Bernardo_Futebol_Clube.png',
    'portuguesa': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Portuguesa_Santista.png/150px-Portuguesa_Santista.png',
    'veloclube': 'https://upload.wikimedia.org/wikipedia/pt/thumb/f/f0/Velo_Clube.png/150px-Velo_Clube.png',
    'flamengo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Flamengo-RJ_%28BRA%29.png/150px-Flamengo-RJ_%28BRA%29.png',
    'vasco': 'https://upload.wikimedia.org/wikipedia/pt/thumb/8/8b/EscudoDoVascoDaGama.svg/150px-EscudoDoVascoDaGama.svg.png',
    'fluminense': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Fluminense_FC_escudo.png/150px-Fluminense_FC_escudo.png',
    'botafogo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Botafogo_de_Futebol_e_Regatas_logo.svg/150px-Botafogo_de_Futebol_e_Regatas_logo.svg.png',
    'bangu': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Bangu_Atl%C3%A9tico_Clube.svg/150px-Bangu_Atl%C3%A9tico_Clube.svg.png',
    'boavista': 'https://upload.wikimedia.org/wikipedia/pt/thumb/1/10/Boavista_Sport_Club.png/150px-Boavista_Sport_Club.png',
    'madureira': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Madureira_Esporte_Clube.png/150px-Madureira_Esporte_Clube.png',
    'novaiguacu': 'https://upload.wikimedia.org/wikipedia/pt/thumb/8/8e/Nova_Igua%C3%A7u_Futebol_Clube.png/150px-Nova_Igua%C3%A7u_Futebol_Clube.png',
    'portuguesa-rj': 'https://upload.wikimedia.org/wikipedia/pt/thumb/3/30/Portuguesa-RJ.png/150px-Portuguesa-RJ.png',
    'sampaiocorrea': 'https://upload.wikimedia.org/wikipedia/pt/thumb/7/74/Sampaio_Corr%C3%AAa_FC.png/150px-Sampaio_Corr%C3%AAa_FC.png',
    'voltaredonda': 'https://upload.wikimedia.org/wikipedia/pt/thumb/2/21/Volta_Redonda_FC.png/150px-Volta_Redonda_FC.png',
    'marica': 'https://upload.wikimedia.org/wikipedia/pt/thumb/c/c0/Maric%C3%A1_FC.png/150px-Maric%C3%A1_FC.png',
    'atletico-mg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Atletico_mineiro_galo.png/150px-Atletico_mineiro_galo.png',
    'cruzeiro': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Cruzeiro_Esporte_Clube_%28logo%29.svg/150px-Cruzeiro_Esporte_Clube_%28logo%29.svg.png',
    'gremio': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Gremio_logo.svg/150px-Gremio_logo.svg.png',
    'internacional': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Sport_Club_Internacional_logo.svg/150px-Sport_Club_Internacional_logo.svg.png',
    'athletico-pr': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Athletico_Paranaense_%28Logo_2019%29.svg/150px-Athletico_Paranaense_%28Logo_2019%29.svg.png',
    'bahia': 'https://upload.wikimedia.org/wikipedia/pt/9/90/ECBahia.png',
    'fortaleza': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Fortaleza_Esporte_Clube_logo.png/150px-Fortaleza_Esporte_Clube_logo.png',
}

def load_teams_from_json():
    """Load teams from data/teams.json"""
    teams_json_path = DATA_DIR / 'teams.json'
    if not teams_json_path.exists():
        print("[WARN] teams.json not found at: " + str(teams_json_path))
        return []

    with open(teams_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data.get('teams', [])

# League Information
CAMPEONATOS = {
    'paulistao': 'https://pt.wikipedia.org/wiki/Campeonato_Paulista_de_Futebol_de_2026',
    'carioca': 'https://pt.wikipedia.org/wiki/Campeonato_Carioca_de_Futebol_de_2026',
    'mineiro': 'https://pt.wikipedia.org/wiki/Campeonato_Mineiro_de_Futebol_de_2026_-_M%C3%B3dulo_I',
    'brasileirao': 'https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_2026_-_S%C3%A9rie_A',
    'libertadores': 'https://pt.wikipedia.org/wiki/Copa_Libertadores_da_Am%C3%A9rica_de_2026',
    'copa-brasil': 'https://pt.wikipedia.org/wiki/Copa_do_Brasil_de_Futebol_de_2026',
}

# League logos
CAMPEONATOS_LOGOS = {
    'paulistao': 'https://upload.wikimedia.org/wikipedia/pt/1/1c/Paulist%C3%A3o_2026.png',
    'carioca': 'https://upload.wikimedia.org/wikipedia/pt/thumb/e/e3/Campeonato_Carioca_logo.png/150px-Campeonato_Carioca_logo.png',
    'mineiro': 'https://upload.wikimedia.org/wikipedia/pt/thumb/4/4f/Campeonato_Mineiro_logo.png/150px-Campeonato_Mineiro_logo.png',
    'brasileirao': 'https://upload.wikimedia.org/wikipedia/pt/thumb/3/3f/Brasileir%C3%A3o_2024_logo.png/150px-Brasileir%C3%A3o_2024_logo.png',
    'libertadores': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/CONMEBOL_Libertadores_logo.svg/150px-CONMEBOL_Libertadores_logo.svg.png',
    'copa-brasil': 'https://upload.wikimedia.org/wikipedia/pt/thumb/8/8f/Copa_do_Brasil_logo.png/150px-Copa_do_Brasil_logo.png',
}

# Channel logos
CANAIS_LOGOS = {
    'sportv': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Star%2B_logo_2021.svg/120px-Star%2B_logo_2021.svg.png',
    'globo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Logotipo_da_Rede_Globo.svg/150px-Logotipo_da_Rede_Globo.svg.png',
    'record': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Rede_Record_logo.svg/150px-Rede_Record_logo.svg.png',
    'band': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Band_logo_2024.svg/150px-Band_logo_2024.svg.png',
    'sbt': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/SBT_logo_2023.svg/150px-SBT_logo_2023.svg.png',
    'cazetv': 'https://upload.wikimedia.org/wikipedia/pt/2/22/Logotipo_da_Caz%C3%A9TV.png',
}

def download_image(url, filepath, retries=3):
    """Download an image from URL"""
    for attempt in range(retries):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print("[OK] Downloaded: " + filepath.name)
            return True
            
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                print("[RETRY] Attempt " + str(attempt + 1) + "/" + str(retries) + " for " + filepath.name)
                time.sleep(1)
            else:
                print("[FAIL] Failed to download " + filepath.name + ": " + str(e))
                return False
    
    return False

def download_team_logos_from_json():
    """Download logos for teams defined in teams.json"""
    teams = load_teams_from_json()
    if not teams:
        print("[WARN] No teams found in teams.json")
        return 0, 0

    print("[TEAMS] Downloading logos for " + str(len(teams)) + " teams from teams.json...")
    print("-" * 60)

    success_count = 0
    skipped_count = 0

    for team in teams:
        team_id = team.get('id', '')
        team_name = team.get('name', '')

        if not team_id:
            continue

        # Check if we have a logo URL for this team
        if team_id in TEAMS_LOGOS:
            url = TEAMS_LOGOS[team_id]
            filepath = TIMES_DIR / (team_id + ".png")

            # Skip if file already exists
            if filepath.exists():
                print("[SKIP] Logo already exists: " + team_id + ".png")
                skipped_count += 1
                continue

            if download_image(url, filepath):
                success_count += 1
            time.sleep(0.5)
        else:
            print("[MISS] No logo URL defined for: " + team_id + " (" + team_name + ")")

    return success_count, skipped_count

def download_all_logos():
    """Download all logos"""
    print("=" * 60)
    print("ONDE VAI PASSAR FUTEBOL HOJE - Logo Downloader")
    print("=" * 60)
    print()

    # Download team logos from teams.json
    print("[TEAMS] Downloading team logos from teams.json...")
    print("-" * 60)
    json_success, json_skipped = download_team_logos_from_json()
    print("\n[STATS] Teams from JSON: " + str(json_success) + " downloaded, " + str(json_skipped) + " skipped\n")

    # Download additional team logos from TEAMS_LOGOS dict
    print("[TEAMS] Downloading additional team logos...")
    print("-" * 60)
    success_count = 0
    for team_id, url in TEAMS_LOGOS.items():
        filepath = TIMES_DIR / (team_id + ".png")
        if filepath.exists():
            continue  # Skip if already downloaded
        if download_image(url, filepath):
            success_count += 1
        time.sleep(0.5)

    print("\n[STATS] Additional teams: " + str(success_count) + " downloaded\n")
    
    # Download league logos
    print("[LEAGUES] Downloading league logos...")
    print("-" * 60)
    success_count = 0
    for league_name, url in CAMPEONATOS_LOGOS.items():
        filepath = CAMPEONATOS_DIR / (league_name + ".png")
        if download_image(url, filepath):
            success_count += 1
        time.sleep(0.5)
    
    print("\n[STATS] Leagues: " + str(success_count) + "/" + str(len(CAMPEONATOS_LOGOS)) + " downloaded successfully\n")
    
    # Download channel logos
    print("[CHANNELS] Downloading channel logos...")
    print("-" * 60)
    success_count = 0
    for channel_name, url in CANAIS_LOGOS.items():
        filepath = CANAIS_DIR / (channel_name + ".png")
        if download_image(url, filepath):
            success_count += 1
        time.sleep(0.5)
    
    print("\n[STATS] Channels: " + str(success_count) + "/" + str(len(CANAIS_LOGOS)) + " downloaded successfully\n")
    
    print("=" * 60)
    print("[SUCCESS] Logo download complete!")
    print("[INFO] Logos saved to: " + str(ASSETS_DIR))
    print("=" * 60)

def list_downloaded_logos():
    """List all downloaded logos"""
    print("\n[LIST] Downloaded logos:")
    print("-" * 60)
    
    for category, directory in [("Teams", TIMES_DIR), ("Leagues", CAMPEONATOS_DIR), ("Channels", CANAIS_DIR)]:
        files = list(directory.glob("*.png"))
        print("\n" + category + " (" + str(len(files)) + " files):")
        for file in sorted(files):
            size_kb = file.stat().st_size / 1024
            print("  - " + file.name + " (" + str(round(size_kb, 1)) + " KB)")

if __name__ == "__main__":
    try:
        download_all_logos()
        list_downloaded_logos()
        
        print("\n[NEXT] Next steps:")
        print("  1. Run: python spiders/update_logo_paths.py")
        print("  2. This will update HTML/JS files to use local logos")
        
    except KeyboardInterrupt:
        print("\n\n[WARN] Download interrupted by user")
    except Exception as e:
        print("\n\n[ERROR] Error: " + str(e))
