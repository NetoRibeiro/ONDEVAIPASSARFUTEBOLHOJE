// ============================================
// ONDE VAI PASSAR FUTEBOL HOJE - App Logic
// ============================================

// === MOCK DATA ===
const mockMatches = [
  {
    id: 1,
    homeTeam: {
      name: 'Flamengo',
      logo: 'assets/times/flamengo.png'
    },
    awayTeam: {
      name: 'Vasco',
      logo: 'assets/times/vasco.png'
    },
    time: '16:00',
    league: 'Campeonato Carioca',
    isLive: true,
    channels: [
      { name: 'SporTV', logo: 'assets/canais/sportv.png' },
      { name: 'Premiere', logo: '' }
    ],
    slug: 'flamengo-x-vasco-16-jan-2026'
  },
  {
    id: 2,
    homeTeam: {
      name: 'Palmeiras',
      logo: 'assets/times/palmeiras.png'
    },
    awayTeam: {
      name: 'Corinthians',
      logo: 'assets/times/corinthians.png'
    },
    time: '18:30',
    league: 'Paulistão',
    isLive: false,
    channels: [
      { name: 'Record', logo: '' },
      { name: 'CazéTV', logo: '' }
    ],
    slug: 'palmeiras-x-corinthians-16-jan-2026'
  },
  {
    id: 3,
    homeTeam: {
      name: 'São Paulo',
      logo: 'assets/times/sao-paulo.png'
    },
    awayTeam: {
      name: 'Santos',
      logo: 'assets/times/santos.png'
    },
    time: '20:00',
    league: 'Paulistão',
    isLive: false,
    channels: [
      { name: 'TNT Sports', logo: '' },
      { name: 'Max', logo: '' }
    ],
    slug: 'sao-paulo-x-santos-16-jan-2026'
  },
  {
    id: 4,
    homeTeam: {
      name: 'Botafogo',
      logo: 'assets/times/botafogo.png'
    },
    awayTeam: {
      name: 'Fluminense',
      logo: 'assets/times/fluminense.png'
    },
    time: '21:30',
    league: 'Campeonato Carioca',
    isLive: false,
    channels: [
      { name: 'Band', logo: '' },
      { name: 'SporTV', logo: 'assets/canais/sportv.png' }
    ],
    slug: 'botafogo-x-fluminense-16-jan-2026'
  },
  {
    id: 5,
    homeTeam: {
      name: 'Atlético-MG',
      logo: 'assets/times/atletico-mg.png'
    },
    awayTeam: {
      name: 'Cruzeiro',
      logo: 'assets/times/cruzeiro.png'
    },
    time: '19:00',
    league: 'Campeonato Mineiro',
    isLive: false,
    channels: [
      { name: 'Globo', logo: '' },
      { name: 'Premiere', logo: '' }
    ],
    slug: 'atletico-mg-x-cruzeiro-16-jan-2026'
  }
];

// === STATE MANAGEMENT ===
let currentDate = new Date();
let filteredMatches = [...mockMatches];
let activeFilter = 'todos';

// === DOM ELEMENTS ===
const elements = {
  searchInput: document.getElementById('searchInput'),
  currentDateEl: document.getElementById('currentDate'),
  prevDayBtn: document.getElementById('prevDay'),
  nextDayBtn: document.getElementById('nextDay'),
  matchesContainer: document.getElementById('matchesContainer'),
  emptyState: document.getElementById('emptyState'),
  loadingState: document.getElementById('loadingState'),
  quickAccessChips: document.querySelectorAll('.team-chip')
};

// === UTILITY FUNCTIONS ===
function formatDate(date) {
  const options = { weekday: 'long', day: 'numeric', month: 'short' };
  const formatted = date.toLocaleDateString('pt-BR', options);
  
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  
  if (date.toDateString() === today.toDateString()) {
    return 'Hoje, ' + date.toLocaleDateString('pt-BR', { day: 'numeric', month: 'short' });
  } else if (date.toDateString() === tomorrow.toDateString()) {
    return 'Amanhã, ' + date.toLocaleDateString('pt-BR', { day: 'numeric', month: 'short' });
  }
  
  return formatted.charAt(0).toUpperCase() + formatted.slice(1);
}

function normalizeString(str) {
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

// === MATCH CARD COMPONENT ===
function createMatchCard(match) {
  const liveIndicator = match.isLive 
    ? `<div class="live-indicator">
         <span class="live-dot"></span>
         AO VIVO
       </div>`
    : '';
  
  const channelBadges = match.channels.map(channel => {
    const logoHtml = channel.logo 
      ? `<img src="${channel.logo}" alt="${channel.name}" class="channel-logo">`
      : '';
    return `
      <span class="channel-badge">
        ${logoHtml}
        ${channel.name}
      </span>
    `;
  }).join('');
  
  return `
    <article class="match-card ${match.isLive ? 'live' : ''}" data-match-id="${match.id}">
      <div class="match-header">
        <div class="match-time">
          <span class="time">${match.time}</span>
          <span class="league">${match.league}</span>
        </div>
        ${liveIndicator}
      </div>
      
      <div class="match-teams">
        <div class="team">
          <img src="${match.homeTeam.logo}" alt="${match.homeTeam.name}" class="team-logo">
          <span class="team-name">${match.homeTeam.name}</span>
        </div>
        
        <span class="vs">VS</span>
        
        <div class="team">
          <img src="${match.awayTeam.logo}" alt="${match.awayTeam.name}" class="team-logo">
          <span class="team-name">${match.awayTeam.name}</span>
        </div>
      </div>
      
      <div class="match-broadcast">
        <span class="broadcast-label">Onde Assistir:</span>
        <div class="channels">
          ${channelBadges}
        </div>
      </div>
    </article>
  `;
}

// === RENDER FUNCTIONS ===
function renderMatches(matches) {
  elements.matchesContainer.innerHTML = '';
  
  if (matches.length === 0) {
    elements.emptyState.classList.remove('hidden');
    elements.matchesContainer.classList.add('hidden');
    return;
  }
  
  elements.emptyState.classList.add('hidden');
  elements.matchesContainer.classList.remove('hidden');
  
  // Sort matches by time
  const sortedMatches = [...matches].sort((a, b) => {
    const timeA = a.time.split(':').map(Number);
    const timeB = b.time.split(':').map(Number);
    return (timeA[0] * 60 + timeA[1]) - (timeB[0] * 60 + timeB[1]);
  });
  
  sortedMatches.forEach(match => {
    elements.matchesContainer.innerHTML += createMatchCard(match);
  });
  
  // Add click handlers to match cards
  document.querySelectorAll('.match-card').forEach(card => {
    card.addEventListener('click', () => {
      const matchId = card.dataset.matchId;
      const match = mockMatches.find(m => m.id == matchId);
      if (match) {
        navigateToMatchDetail(match);
      }
    });
  });
}

function updateDateDisplay() {
  elements.currentDateEl.textContent = formatDate(currentDate);
}

// === FILTER & SEARCH FUNCTIONS ===
function filterMatches(searchTerm = '', teamFilter = 'todos') {
  let matches = [...mockMatches];
  
  // Filter by team
  if (teamFilter !== 'todos') {
    matches = matches.filter(match => {
      const homeTeamNorm = normalizeString(match.homeTeam.name);
      const awayTeamNorm = normalizeString(match.awayTeam.name);
      const filterNorm = normalizeString(teamFilter);
      return homeTeamNorm.includes(filterNorm) || awayTeamNorm.includes(filterNorm);
    });
  }
  
  // Filter by search term
  if (searchTerm) {
    const searchNorm = normalizeString(searchTerm);
    matches = matches.filter(match => {
      const homeTeamNorm = normalizeString(match.homeTeam.name);
      const awayTeamNorm = normalizeString(match.awayTeam.name);
      const leagueNorm = normalizeString(match.league);
      const channelsNorm = match.channels.map(c => normalizeString(c.name)).join(' ');
      
      return homeTeamNorm.includes(searchNorm) ||
             awayTeamNorm.includes(searchNorm) ||
             leagueNorm.includes(searchNorm) ||
             channelsNorm.includes(searchNorm);
    });
  }
  
  filteredMatches = matches;
  renderMatches(filteredMatches);
}

// === NAVIGATION ===
function navigateToMatchDetail(match) {
  // In a real implementation, this would navigate to a detail page
  // For now, we'll just show an alert
  alert(`Navegando para: /onde-assistir-${match.slug}\n\nEsta página mostraria:\n- Escalações completas\n- Estatísticas do confronto\n- Todos os canais de transmissão\n- Histórico entre os times`);
}

// === EVENT HANDLERS ===
function handleSearch(e) {
  const searchTerm = e.target.value;
  filterMatches(searchTerm, activeFilter);
}

function handleTeamFilter(e) {
  const chip = e.target.closest('.team-chip');
  if (!chip) return;
  
  const team = chip.dataset.team;
  
  // Update active state
  elements.quickAccessChips.forEach(c => c.classList.remove('active'));
  chip.classList.add('active');
  
  activeFilter = team;
  filterMatches(elements.searchInput.value, team);
}

function handleDateChange(direction) {
  if (direction === 'prev') {
    currentDate.setDate(currentDate.getDate() - 1);
  } else {
    currentDate.setDate(currentDate.getDate() + 1);
  }
  
  updateDateDisplay();
  
  // In a real app, this would fetch matches for the new date
  // For now, we'll just show a loading state briefly
  elements.loadingState.classList.remove('hidden');
  elements.matchesContainer.classList.add('hidden');
  
  setTimeout(() => {
    elements.loadingState.classList.add('hidden');
    renderMatches(filteredMatches);
  }, 500);
}

// === INITIALIZATION ===
function init() {
  // Set initial date
  updateDateDisplay();
  
  // Render initial matches
  renderMatches(mockMatches);
  
  // Set first chip as active
  if (elements.quickAccessChips.length > 0) {
    elements.quickAccessChips[0].classList.add('active');
  }
  
  // Event listeners
  elements.searchInput.addEventListener('input', handleSearch);
  elements.prevDayBtn.addEventListener('click', () => handleDateChange('prev'));
  elements.nextDayBtn.addEventListener('click', () => handleDateChange('next'));
  
  // Quick access chips
  document.getElementById('quickAccess').addEventListener('click', handleTeamFilter);
  
  console.log('⚽ Onde Vai Passar Futebol Hoje - Initialized');
  console.log(`📅 Showing ${mockMatches.length} matches for ${formatDate(currentDate)}`);
}

// Start the app when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
