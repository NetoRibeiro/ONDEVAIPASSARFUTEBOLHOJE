# -*- coding: utf-8 -*-
"""
Team Page Generator from Wikipedia League Data
Scrapes Wikipedia league pages and creates individual team pages
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
import re
import json

# Base directories
BASE_DIR = Path(__file__).parent.parent
TEAMS_DIR = BASE_DIR / 'times'
DATA_DIR = BASE_DIR / 'data'
TEAMS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
# UF: Apelido do Campeonato, Nome do Campeonato, Nome real do Campeonato, Link da Federação, Link do Campeonato na Federação, Pagina do Campeonato na WikiPedia

TEAMS = {
    'Athletico Paranaense': 'https://pt.wikipedia.org/wiki/Club_Athletico_Paranaense',
    'Atlético Mineiro': 'https://pt.wikipedia.org/wiki/Clube_Atlético_Mineiro',
    'Bahia': 'https://pt.wikipedia.org/wiki/Esporte_Clube_Bahia',
    'Botafogo': 'https://pt.wikipedia.org/wiki/Botafogo_de_Futebol_e_Regatas',
    'Chapecoense': 'https://pt.wikipedia.org/wiki/Associação_Chapecoense_de_Futebol',
    'Corinthians': 'https://pt.wikipedia.org/wiki/Sport_Club_Corinthians_Paulista',
    'Coritiba': 'https://pt.wikipedia.org/wiki/Coritiba_Foot_Ball_Club',
    'Cruzeiro': 'https://pt.wikipedia.org/wiki/Cruzeiro_Esporte_Clube',
    'Flamengo': 'https://pt.wikipedia.org/wiki/Clube_de_Regatas_do_Flamengo',
    'Fluminense': 'https://pt.wikipedia.org/wiki/Fluminense_Football_Club',
    'Grêmio': 'https://pt.wikipedia.org/wiki/Grêmio_Foot-Ball_Porto_Alegrense',
    'Internacional': 'https://pt.wikipedia.org/wiki/Sport_Club_Internacional',
    'Mirassol': 'https://pt.wikipedia.org/wiki/Mirassol_Futebol_Clube',
    'Palmeiras': 'https://pt.wikipedia.org/wiki/Sociedade_Esportiva_Palmeiras',
    'Red Bull Bragantino': 'https://pt.wikipedia.org/wiki/Red_Bull_Bragantino',
    'Remo': 'https://pt.wikipedia.org/wiki/Clube_do_Remo',
    'Santos': 'https://pt.wikipedia.org/wiki/Santos_Futebol_Clube',
    'São Paulo': 'https://pt.wikipedia.org/wiki/São_Paulo_Futebol_Clube',
    'Vasco da Gama': 'https://pt.wikipedia.org/wiki/Club_de_Regatas_Vasco_da_Gama',
    'Vitória': 'https://pt.wikipedia.org/wiki/Esporte_Clube_Vitória'
}

LEAGUES = ["brasileiro26"]

def slugify(text):
    """Convert team name to URL-friendly slug"""
    text = text.lower()
    text = text.replace('ã', 'a').replace('á', 'a').replace('â', 'a')
    text = text.replace('é', 'e').replace('ê', 'e')
    text = text.replace('í', 'i')
    text = text.replace('ó', 'o').replace('õ', 'o').replace('ô', 'o')
    text = text.replace('ú', 'u')
    text = text.replace('ç', 'c')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def load_teams_json():
    """Load existing teams from data/teams.json"""
    teams_json_path = DATA_DIR / 'teams.json'
    if not teams_json_path.exists():
        return {"teams": []}

    with open(teams_json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_teams_json(data):
    """Save teams data to data/teams.json"""
    teams_json_path = DATA_DIR / 'teams.json'
    with open(teams_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("[OK] Updated teams.json with " + str(len(data.get('teams', []))) + " teams")

def get_team_by_id(teams_data, team_id):
    """Find a team by ID in the teams list"""
    for team in teams_data.get('teams', []):
        if team.get('id') == team_id:
            return team
    return None

def add_or_update_team(teams_data, team_info, tournaments_to_add):
    """Add a new team or update existing team's tournaments

    Args:
        teams_data: The teams.json data structure
        team_info: Team information dict
        tournaments_to_add: List of tournament IDs to add

    Returns:
        tuple: (is_new_team, tournaments_added)
    """
    team_id = team_info.get('id')
    existing_team = get_team_by_id(teams_data, team_id)

    if existing_team:
        # Update tournaments if not already present
        tournaments_added = []
        for tournament_id in tournaments_to_add:
            if tournament_id and tournament_id not in existing_team.get('tournaments', []):
                existing_team.setdefault('tournaments', []).append(tournament_id)
                tournaments_added.append(tournament_id)
        return False, tournaments_added  # Not a new team
    else:
        # Add new team
        new_team = {
            "id": team_id,
            "name": team_info.get('name'),
            "slug": team_info.get('slug', team_id),
            "logo": "/assets/times/" + team_id + ".png",
            "state": team_info.get('state', ''),
            "stadium": team_info.get('stadium', ''),
            "founded": team_info.get('founded', 0),
            "tournaments": list(tournaments_to_add) if tournaments_to_add else [],
            "colors": {
                "primary": "#000000",
                "secondary": "#FFFFFF"
            }
        }
        teams_data['teams'].append(new_team)
        return True, tournaments_to_add  # New team added

def extract_teams_from_league(url, league_name):
    """Extract team names and Wikipedia URLs from league page"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        teams = {}  # Changed to dict to store team data
        
        # Look for tables with team information
        tables = soup.find_all('table', {'class': 'wikitable'})
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                for cell in cells:
                    # Look for links to team pages
                    links = cell.find_all('a')
                    for link in links:
                        href = link.get('href', '')
                        title = link.get('title', '')
                        text = link.get_text(strip=True)
                        
                        # Filter for team links (exclude references, years, etc.)
                        if href.startswith('/wiki/') and not any(x in href for x in ['Ficheiro:', 'File:', 'Categoria:', 'Category:', 'Wikipedia:', 'Ajuda:']):
                            if len(text) > 2 and not text.isdigit() and 'futebol' not in text.lower():
                                # Common team indicators
                                if any(x in text for x in ['FC', 'SC', 'EC', 'AC', 'Clube', 'Esporte', 'Sport', 'Futebol']):
                                    wiki_url = 'https://pt.wikipedia.org' + href
                                    teams[text] = {'name': text, 'wiki_url': wiki_url, 'wiki_title': title}
                                elif any(x in title for x in ['Futebol', 'Clube']):
                                    wiki_url = 'https://pt.wikipedia.org' + href
                                    teams[text] = {'name': text, 'wiki_url': wiki_url, 'wiki_title': title}
        
        print("[INFO] Found " + str(len(teams)) + " teams in " + league_name)
        return teams
        
    except Exception as e:
        print("[ERROR] Failed to extract teams from " + league_name + ": " + str(e))
        return {}

def create_team_page(team_data, league_name):
    """Create an HTML page for a team"""
    team_name = team_data['name']
    wiki_url = team_data.get('wiki_url', '')
    
    slug = slugify(team_name)
    filepath = TEAMS_DIR / (slug + ".html")
    
    # Skip if page already exists
    if filepath.exists():
        print("[SKIP] Page already exists: " + slug + ".html")
        return False
    
    # Create HTML content
    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<!-- Wikipedia Source: {wiki_url} -->
<!-- Team Data: {{"name": "{team_name}", "league": "{league_name}", "slug": "{slug}"}} -->
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- SEO Meta Tags -->
  <title>{team_name} - Jogos, Escalação e Onde Assistir | Onde Vai Passar Futebol Hoje</title>
  <meta name="description" content="Veja todos os jogos do {team_name}, escalações, estatísticas e onde assistir ao vivo. Acompanhe o {team_name} no {league_name}.">
  <meta name="keywords" content="{team_name}, {team_name} jogos, {team_name} onde assistir, {team_name} escalação, {league_name}">
  
  <!-- Favicon -->
  <link rel="icon" type="image/png" href="../assets/favicon.png">
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
  
  <!-- Stylesheet -->
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  
  <!-- Header -->
  <header class="header">
    <div class="container">
      <div class="header-content">
        <div class="header-top">
          <h1 class="logo">
            <a href="../index.html" style="color: inherit;">⚽ Futebol Hoje</a>
          </h1>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="container">
    
    <!-- Breadcrumb -->
    <nav class="breadcrumb" aria-label="Breadcrumb" style="padding: 1rem 0; font-size: 0.875rem; color: #BDBDBD;">
      <a href="../index.html" style="color: #FFD700;">Início</a>
      <span style="margin: 0 0.5rem;">›</span>
      <a href="../campeonatos.html" style="color: #FFD700;">Campeonatos</a>
      <span style="margin: 0 0.5rem;">›</span>
      <span>{team_name}</span>
    </nav>
    
    <!-- Team Hero -->
    <div style="background: linear-gradient(135deg, rgba(0, 26, 51, 0.9), rgba(0, 8, 20, 0.9)); border: 2px solid #FFD700; border-radius: 16px; padding: 2rem; margin-bottom: 2rem; text-align: center;">
      <h1 style="font-size: 2.25rem; color: #F2FF00; margin-bottom: 1rem;">{team_name}</h1>
      <p style="color: #BDBDBD; font-size: 1.125rem;">{league_name}</p>
    </div>
    
    <!-- Próximos Jogos -->
    <section style="margin-bottom: 2rem;">
      <h2 style="color: #F2FF00; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
        <span style="width: 4px; height: 32px; background: #FFD700; border-radius: 4px;"></span>
        Próximos Jogos
      </h2>
      <div style="background: rgba(0, 26, 51, 0.6); border: 1px solid #424242; border-radius: 12px; padding: 1.5rem; text-align: center; color: #BDBDBD;">
        <p>Informações sobre os próximos jogos do {team_name} serão exibidas aqui.</p>
        <p style="margin-top: 1rem;"><a href="../index.html" style="color: #FFD700;">Ver todos os jogos de hoje</a></p>
      </div>
    </section>
    
    <!-- Últimos Resultados -->
    <section style="margin-bottom: 2rem;">
      <h2 style="color: #F2FF00; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
        <span style="width: 4px; height: 32px; background: #FFD700; border-radius: 4px;"></span>
        Últimos Resultados
      </h2>
      <div style="background: rgba(0, 26, 51, 0.6); border: 1px solid #424242; border-radius: 12px; padding: 1.5rem; text-align: center; color: #BDBDBD;">
        <p>Resultados recentes do {team_name} serão exibidos aqui.</p>
      </div>
    </section>
    
    <!-- Sobre o Time -->
    <section style="margin-bottom: 2rem;">
      <h2 style="color: #F2FF00; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
        <span style="width: 4px; height: 32px; background: #FFD700; border-radius: 4px;"></span>
        Sobre o {team_name}
      </h2>
      <div style="background: rgba(0, 26, 51, 0.6); border: 1px solid #424242; border-radius: 12px; padding: 1.5rem; color: #E0E0E0; line-height: 1.8;">
        <p>O <strong>{team_name}</strong> é um dos times participantes do <strong>{league_name}</strong>.</p>
        <p style="margin-top: 1rem;">Acompanhe todos os jogos, escalações e informações sobre onde assistir o {team_name} ao vivo.</p>
      </div>
    </section>
    
  </main>

  <!-- Footer -->
  <footer style="text-align: center; padding: 2rem 0; color: #BDBDBD; font-size: 0.875rem; margin-top: 2.5rem;">
    <div class="container">
      <p>&copy; 2026 Onde Vai Passar Futebol Hoje. Todos os direitos reservados.</p>
    </div>
  </footer>

</body>
</html>
""".format(team_name=team_name, league_name=league_name, slug=slug, wiki_url=wiki_url)
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("[OK] Created: " + slug + ".html")
    return True

def generate_all_team_pages():
    """Generate team pages using TEAMS dictionary as source"""
    print("=" * 60)
    print("TEAM PAGE GENERATOR - From TEAMS Dictionary")
    print("=" * 60)
    print()

    # Load existing teams.json
    teams_json_data = load_teams_json()
    print("[INFO] Loaded " + str(len(teams_json_data.get('teams', []))) + " existing teams from teams.json")
    print("[INFO] Processing " + str(len(TEAMS)) + " teams from TEAMS dictionary")
    print("-" * 60)

    all_teams = {}
    total_created = 0
    total_skipped = 0
    new_teams_added = 0
    tournaments_updated = 0

    # Iterate over TEAMS dictionary directly
    for team_name, wiki_url in TEAMS.items():
        team_data = {
            'name': team_name,
            'wiki_url': wiki_url
        }

        # Create team page
        if create_team_page(team_data, "Brasileiro"):
            total_created += 1
        else:
            total_skipped += 1

        # Store team info
        all_teams[team_name] = {'leagues': LEAGUES, 'wiki_url': wiki_url}

        # Prepare team info for teams.json
        team_id = slugify(team_name)
        team_info = {
            'id': team_id,
            'name': team_name,
            'slug': team_id,
            'state': '',
            'stadium': '',
            'founded': 0
        }

        # Add or update team in teams.json with all LEAGUES
        is_new, added_tournaments = add_or_update_team(teams_json_data, team_info, LEAGUES)
        if is_new:
            new_teams_added += 1
            print("[NEW] Added to teams.json: " + team_name)
        elif added_tournaments:
            tournaments_updated += 1
            print("[UPDATE] Added tournaments " + str(added_tournaments) + " to: " + team_name)

        time.sleep(0.5)  # Small delay

    print("\n" + "=" * 60)
    print("[SUCCESS] Team page generation complete!")
    print("[STATS] Created: " + str(total_created) + " pages")
    print("[STATS] Skipped: " + str(total_skipped) + " pages (already exist)")
    print("[STATS] New teams added to teams.json: " + str(new_teams_added))
    print("[STATS] Existing teams with tournaments updated: " + str(tournaments_updated))
    print("[INFO] Leagues applied: " + str(LEAGUES))
    print("[INFO] Pages saved to: " + str(TEAMS_DIR))
    print("=" * 60)

    # Save updated teams.json
    save_teams_json(teams_json_data)

    # Save basic team data to JSON (legacy format)
    json_path = DATA_DIR / 'teams_data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_teams, f, ensure_ascii=False, indent=2)
    print("[OK] Saved team data to: " + str(json_path))

    # Create index file
    create_teams_index(all_teams)

def create_teams_index(teams_dict):
    """Create an index page listing all teams"""
    index_path = TEAMS_DIR / "index.html"
    
    teams_html = ""
    for team_name in sorted(teams_dict.keys()):
        slug = slugify(team_name)
        team_info = teams_dict[team_name]
        leagues = ", ".join(team_info.get('leagues', []))
        wiki_url = team_info.get('wiki_url', '')
        teams_html += """
        <div style="background: rgba(0, 26, 51, 0.6); border: 1px solid #424242; border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
          <h3 style="color: #FFD700; margin-bottom: 0.5rem;">
            <a href="{slug}.html" style="color: inherit; text-decoration: none;">{team_name}</a>
          </h3>
          <p style="color: #BDBDBD; font-size: 0.875rem;">Campeonatos: {leagues}</p>
          <p style="color: #757575; font-size: 0.75rem; margin-top: 0.5rem;"><a href="{wiki_url}" target="_blank" style="color: #FFD700;">Wikipedia</a></p>
        </div>
        """.format(slug=slug, team_name=team_name, leagues=leagues, wiki_url=wiki_url)
    
    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Todos os Times | Onde Vai Passar Futebol Hoje</title>
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <header class="header">
    <div class="container">
      <h1 class="logo"><a href="../index.html" style="color: inherit;">⚽ Futebol Hoje</a></h1>
    </div>
  </header>
  <main class="container" style="padding: 2rem 0;">
    <h2 style="color: #F2FF00; margin-bottom: 2rem;">Todos os Times</h2>
    {teams_html}
  </main>
</body>
</html>
""".format(teams_html=teams_html)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("\n[OK] Created teams index: times/index.html")

if __name__ == "__main__":
    try:
        generate_all_team_pages()
        
        print("\n[NEXT] Next steps:")
        print("  1. Check the 'times/' folder for generated pages")
        print("  2. Open times/index.html to see all teams")
        print("  3. Customize team pages with real data from your API")
        
    except KeyboardInterrupt:
        print("\n\n[WARN] Generation interrupted by user")
    except Exception as e:
        print("\n\n[ERROR] Error: " + str(e))
        import traceback
        traceback.print_exc()
