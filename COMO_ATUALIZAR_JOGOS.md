# 📝 Como Atualizar Jogos - Guia Completo

Este guia explica como adicionar, editar e remover jogos usando arquivos JSON.

---

## 📂 Estrutura de Arquivos

Todos os dados estão em arquivos JSON na pasta `/data/`:

```
data/
├── matches.json          # Jogos e partidas
├── teams.json            # Times e informações
└── tournaments.json      # Campeonatos
```

---

## 🎮 1. Como Adicionar um Novo Jogo

### Passo 1: Abra o arquivo `data/matches.json`

### Passo 2: Adicione um novo objeto ao array `matches`

```json
{
  "id": "paulistao26-saopaulo-vs-corinthians-25-01-2026",
  "tournament": "paulistao26",
  "homeTeam": "saopaulo",
  "awayTeam": "corinthians",
  "matchDate": "2026-01-25T21:30:00-03:00",
  "venue": {
    "name": "Morumbi",
    "city": "São Paulo",
    "state": "SP"
  },
  "status": "scheduled",
  "isLive": false,
  "score": {
    "home": null,
    "away": null
  },
  "round": "3ª Rodada",
  "group": "Grupo A vs Grupo C",
  "broadcasting": [
    {
      "channel": "Premiere",
      "logo": "/assets/canais/premiere.png",
      "type": "pay-tv"
    }
  ]
}
```

### 📋 Campos Explicados:

| Campo | Descrição | Exemplo | Obrigatório |
|-------|-----------|---------|-------------|
| `id` | Identificador único | `"paulistao26-saopaulo-vs-corinthians-25-01-2026"` | ✅ Sim |
| `tournament` | ID do campeonato | `"paulistao26"` ou `"carioca26"` | ✅ Sim |
| `homeTeam` | ID do time mandante | `"saopaulo"` | ✅ Sim |
| `awayTeam` | ID do time visitante | `"corinthians"` | ✅ Sim |
| `matchDate` | Data/hora do jogo (ISO 8601) | `"2026-01-25T21:30:00-03:00"` | ✅ Sim |
| `venue.name` | Nome do estádio | `"Morumbi"` | ✅ Sim |
| `venue.city` | Cidade | `"São Paulo"` | ✅ Sim |
| `venue.state` | Estado (sigla) | `"SP"` | ✅ Sim |
| `status` | Status do jogo | `"scheduled"`, `"live"`, `"finished"` | ✅ Sim |
| `isLive` | Jogo ao vivo? | `true` ou `false` | ✅ Sim |
| `score.home` | Gols do mandante | `2` ou `null` (se não iniciado) | ✅ Sim |
| `score.away` | Gols do visitante | `1` ou `null` (se não iniciado) | ✅ Sim |
| `round` | Rodada do campeonato | `"1ª Rodada"` | ❌ Não |
| `group` | Grupo (se aplicável) | `"Grupo A"` | ❌ Não |
| `broadcasting` | Canais de transmissão | Array de objetos | ✅ Sim |

---

## 🔄 2. Como Atualizar um Jogo Existente

### Para atualizar placar de jogo ao vivo:

1. Encontre o jogo pelo `id` em `matches.json`
2. Altere os campos:

```json
{
  "id": "carioca26-flamengo-vs-vasco-20-01-2026",
  "status": "live",
  "isLive": true,
  "score": {
    "home": 2,
    "away": 1
  }
}
```

### Para finalizar um jogo:

```json
{
  "id": "carioca26-flamengo-vs-vasco-20-01-2026",
  "status": "finished",
  "isLive": false,
  "score": {
    "home": 3,
    "away": 2
  }
}
```

---

## 🏆 3. IDs dos Campeonatos Disponíveis

Use estes IDs no campo `tournament`:

| Campeonato | ID |
|------------|-----|
| Campeonato Paulista 2026 | `paulistao26` |
| Campeonato Carioca 2026 | `carioca26` |
| Campeonato Mineiro 2026 | `mineiro26` ⚠️ (em construção) |
| Campeonato Gaúcho 2026 | `gaucho26` ⚠️ (em construção) |

---

## ⚽ 4. IDs dos Times

### Paulistão (16 times):

| Time | ID |
|------|-----|
| São Paulo | `saopaulo` |
| Corinthians | `corinthians` |
| Palmeiras | `palmeiras` |
| Santos | `santos` |
| Red Bull Bragantino | `redballbauru` |
| Ponte Preta | `pontepreta` |
| Guarani | `guarani` |
| Água Santa | `aguasantaense` |
| Botafogo-SP | `botafogosp` |
| Ituano | `ituano` |
| Mirassol | `mirassol` |
| Novorizontino | `novorizontino` |
| São Bernardo | `saobernardo` |
| Inter de Limeira | `interdelimeira` |
| Portuguesa | `portuguesasp` |
| São Caetano | `saocaetano` |

### Carioca (12 times):

| Time | ID |
|------|-----|
| Flamengo | `flamengo` |
| Vasco da Gama | `vasco` |
| Fluminense | `fluminense` |
| Botafogo | `botafogo` |
| Bangu | `bangu` |
| Boavista | `boavista` |
| Madureira | `madureira` |
| Nova Iguaçu | `novaigrj` |
| Portuguesa-RJ | `portuguesa-rj` |
| Sampaio Corrêa | `samaritano` |
| Volta Redonda | `voltaredonda` |
| Audax | `audax` |

---

## 📺 5. Canais de Transmissão

### Estrutura de Broadcasting:

```json
"broadcasting": [
  {
    "channel": "Nome do Canal",
    "logo": "/assets/canais/logo.png",
    "type": "tipo"
  }
]
```

### Tipos de Canal:

| Tipo | Descrição |
|------|-----------|
| `pay-tv` | TV por Assinatura (Premiere, SporTV) |
| `tv-aberta` | TV Aberta (Globo, Record, Band) |
| `streaming` | Streaming (HBO Max, Nosso Futebol) |
| `online` | Online/YouTube |

### Canais Comuns:

```json
// Premiere
{
  "channel": "Premiere",
  "logo": "/assets/canais/premiere.png",
  "type": "pay-tv"
}

// SporTV
{
  "channel": "SporTV",
  "logo": "/assets/canais/sportv.png",
  "type": "pay-tv"
}

// HBO Max
{
  "channel": "HBO Max",
  "logo": "/assets/canais/hbo-max.png",
  "type": "streaming"
}

// Record
{
  "channel": "Record",
  "logo": "/assets/canais/record.png",
  "type": "tv-aberta"
}

// Band
{
  "channel": "Band",
  "logo": "/assets/canais/band.png",
  "type": "tv-aberta"
}

// Nosso Futebol (sem logo)
{
  "channel": "Nosso Futebol",
  "logo": "",
  "type": "streaming"
}

// YouTube
{
  "channel": "YouTube Paulistão",
  "logo": "",
  "type": "online"
}
```

---

## 📅 6. Formato de Data (ISO 8601)

### Estrutura:
```
YYYY-MM-DDTHH:MM:SS-03:00
```

### Exemplos:

| Descrição | Formato |
|-----------|---------|
| 18 Jan 2026 às 21h30 | `2026-01-18T21:30:00-03:00` |
| 20 Jan 2026 às 16h00 | `2026-01-20T16:00:00-03:00` |
| 25 Jan 2026 às 18h30 | `2026-01-25T18:30:00-03:00` |

**Nota:** `-03:00` é o fuso horário de Brasília (BRT)

---

## 🆔 7. Como Criar um ID de Jogo

### Formato:
```
{tournament}-{homeTeam}-vs-{awayTeam}-{dd-mm-yyyy}
```

### Exemplos:

```
paulistao26-saopaulo-vs-corinthians-18-01-2026
carioca26-flamengo-vs-vasco-20-01-2026
paulistao26-palmeiras-vs-santos-22-01-2026
```

### Regras:
- Tudo em minúsculas
- Sem acentos ou caracteres especiais
- Use `-vs-` entre os times
- Data no formato `dd-mm-yyyy`

---

## ✏️ 8. Exemplo Completo: Adicionando 3 Jogos

```json
{
  "matches": [
    {
      "id": "paulistao26-saopaulo-vs-palmeiras-26-01-2026",
      "tournament": "paulistao26",
      "homeTeam": "saopaulo",
      "awayTeam": "palmeiras",
      "matchDate": "2026-01-26T16:00:00-03:00",
      "venue": {
        "name": "Morumbi",
        "city": "São Paulo",
        "state": "SP"
      },
      "status": "scheduled",
      "isLive": false,
      "score": {
        "home": null,
        "away": null
      },
      "round": "4ª Rodada",
      "group": "Clássico",
      "broadcasting": [
        {
          "channel": "Premiere",
          "logo": "/assets/canais/premiere.png",
          "type": "pay-tv"
        },
        {
          "channel": "HBO Max",
          "logo": "/assets/canais/hbo-max.png",
          "type": "streaming"
        }
      ]
    },
    {
      "id": "carioca26-flamengo-vs-fluminense-27-01-2026",
      "tournament": "carioca26",
      "homeTeam": "flamengo",
      "awayTeam": "fluminense",
      "matchDate": "2026-01-27T21:30:00-03:00",
      "venue": {
        "name": "Maracanã",
        "city": "Rio de Janeiro",
        "state": "RJ"
      },
      "status": "scheduled",
      "isLive": false,
      "score": {
        "home": null,
        "away": null
      },
      "round": "4ª Rodada",
      "group": "Fla-Flu",
      "broadcasting": [
        {
          "channel": "Globo",
          "logo": "/assets/canais/globo.png",
          "type": "tv-aberta"
        },
        {
          "channel": "Premiere",
          "logo": "/assets/canais/premiere.png",
          "type": "pay-tv"
        }
      ]
    },
    {
      "id": "paulistao26-corinthians-vs-santos-28-01-2026",
      "tournament": "paulistao26",
      "homeTeam": "corinthians",
      "awayTeam": "santos",
      "matchDate": "2026-01-28T20:00:00-03:00",
      "venue": {
        "name": "Neo Química Arena",
        "city": "São Paulo",
        "state": "SP"
      },
      "status": "scheduled",
      "isLive": false,
      "score": {
        "home": null,
        "away": null
      },
      "round": "4ª Rodada",
      "broadcasting": [
        {
          "channel": "Record",
          "logo": "/assets/canais/record.png",
          "type": "tv-aberta"
        }
      ]
    }
  ]
}
```

---

## ⚠️ 9. Erros Comuns

### ❌ Erro 1: ID duplicado
```json
// ERRADO - Mesmo ID usado duas vezes
{
  "id": "paulistao26-saopaulo-vs-corinthians-18-01-2026",
  ...
}
```
**Solução:** Cada jogo precisa ter um ID único.

---

### ❌ Erro 2: Time não existe
```json
// ERRADO - Time não está em teams.json
{
  "homeTeam": "gremio",
  ...
}
```
**Solução:** Use apenas IDs de times que existem em `teams.json`. Grêmio não está no Paulistão ou Carioca.

---

### ❌ Erro 3: Data inválida
```json
// ERRADO - Formato incorreto
{
  "matchDate": "25/01/2026 21:30",
  ...
}
```
**Solução:** Use formato ISO 8601: `"2026-01-25T21:30:00-03:00"`

---

### ❌ Erro 4: Vírgula faltando
```json
{
  "id": "...",
  "tournament": "paulistao26"  // ❌ Falta vírgula aqui
  "homeTeam": "saopaulo"
}
```
**Solução:** Adicione vírgula após cada campo (exceto o último do objeto).

---

### ❌ Erro 5: Status incorreto
```json
// ERRADO - Status não válido
{
  "status": "agendado",
  ...
}
```
**Solução:** Use apenas: `"scheduled"`, `"live"`, ou `"finished"`

---

## 🔧 10. Dicas e Boas Práticas

### ✅ Use um editor JSON
- **VS Code:** Valida JSON automaticamente
- **JSONLint:** https://jsonlint.com/ (validador online)
- **JSON Editor Online:** https://jsoneditoronline.org/

### ✅ Sempre faça backup
Antes de editar, copie o arquivo `matches.json`:
```
matches.json → matches.backup.json
```

### ✅ Teste localmente
Depois de editar, abra `index.html` no navegador para ver se funciona.

### ✅ Ordem cronológica
Organize os jogos por data para facilitar encontrar jogos futuros.

### ✅ Remova jogos antigos
Periodicamente, remova jogos de datas passadas para manter o arquivo leve.

---

## 🚀 11. Workflow Recomendado

### Para atualizar jogos diariamente:

1. **Manhã (Adicionar novos jogos)**
   - Abra `matches.json`
   - Adicione jogos do dia
   - Salve e teste

2. **Durante o dia (Atualizar ao vivo)**
   - Encontre o jogo pelo `id`
   - Altere `isLive: true`
   - Atualize `score`
   - Salve

3. **Fim do dia (Finalizar jogos)**
   - Altere `status: "finished"`
   - Altere `isLive: false`
   - Placar final em `score`

---

## 📊 12. Exemplo: Jogo Ao Vivo

### Antes do jogo (Agendado):
```json
{
  "id": "carioca26-flamengo-vs-vasco-20-01-2026",
  "status": "scheduled",
  "isLive": false,
  "score": {
    "home": null,
    "away": null
  }
}
```

### Durante o jogo (Ao Vivo - 30 minutos):
```json
{
  "id": "carioca26-flamengo-vs-vasco-20-01-2026",
  "status": "live",
  "isLive": true,
  "score": {
    "home": 1,
    "away": 0
  }
}
```

### Após o jogo (Finalizado):
```json
{
  "id": "carioca26-flamengo-vs-vasco-20-01-2026",
  "status": "finished",
  "isLive": false,
  "score": {
    "home": 3,
    "away": 2
  }
}
```

---

## 📞 13. Precisa de Ajuda?

### Validação JSON:
- Use: https://jsonlint.com/
- Cole seu JSON e clique em "Validate JSON"

### Erros comuns:
- **Unexpected token:** Vírgula faltando ou sobrando
- **Unexpected end of JSON:** Chave `}` faltando
- **Invalid character:** Aspas erradas (use `"` e não `'`)

---

## 📝 14. Checklist Antes de Salvar

- [ ] Todos os IDs são únicos?
- [ ] Times existem em `teams.json`?
- [ ] Campeonatos existem em `tournaments.json`?
- [ ] Datas no formato ISO 8601?
- [ ] Status é válido? (`scheduled`, `live`, `finished`)
- [ ] JSON válido? (teste em jsonlint.com)
- [ ] Vírgulas corretas?
- [ ] Salvou o arquivo?
- [ ] Testou no navegador?

---

**Dica Final:** Sempre valide seu JSON antes de salvar. Um erro de sintaxe pode quebrar todo o site!

🎯 **Bom trabalho atualizando os jogos!**
