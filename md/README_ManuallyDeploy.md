# 🚀 Deploy VPS Hostinger com Easypanel

Este guia explica como colocar o site **Onde Vai Passar Futebol Hoje** no ar usando o **Easypanel** na sua VPS Hostinger. O Easypanel facilita muito o gerenciamento via interface visual (Docker).

## 📋 Pré-requisitos
- VPS Hostinger com **Easypanel** instalado.
- Domínio **ONDEVAIPASSARFUTEBOLHOJE.COM.BR** configurado no Registro.br.
- Projeto no GitHub.

---

## 🌐 Passo 1: Configurar DNS (Registro.br)

Acesse o painel do Registro.br e aponte o seu domínio para o IP da sua VPS:

1.  Crie uma entrada do tipo **A** com o nome `@` (ou vazio) apontando para o **IP da sua VPS**.
2.  Crie uma entrada do tipo **A** (ou CNAME) com o nome `www` também para o **IP da sua VPS**.

---

## 🏗️ Passo 2: Criar o Serviço no Easypanel

1.  Acesse o painel do seu Easypanel (geralmente `https://ip-da-sua-vps:3000`).
2.  Crie um novo **Project** (ex: `FutebolHoje`).
3.  Dentro do projeto, clique em **+ Service** e escolha **App**.
4.  Dê um nome ao serviço (ex: `site-principal`).

---

## 📁 Passo 3: Conectar ao GitHub

No menu **Source** do seu serviço no Easypanel:

1.  Selecione **GitHub**.
2.  Conecte sua conta e selecione o repositório `ONDEVAIPASSARFUTEBOLHOJE`.
3.  A branch deve ser `main`.
4.  Ative o **Auto Deploy** (para que o site atualize sempre que você der `git push`).

---

## 🛠️ Passo 4: Configurar Build (Nixpacks)

No Easypanel, o **Nixpacks** tentará detectar seu site sozinho. Com base na sua tela, preencha assim:

1.  **Versão**: Pode manter a que já está (ex: `1.41.0`).
2.  **Comando de Instalação**: Deixe **vazio**.
3.  **Comando de Build**: Deixe **vazio** (pois você já gerou as páginas localmente e deu Push).
4.  **Comando de Início**: Deixe **vazio**. (O Nixpacks detectará o `index.html` e usará um servidor Nginx interno).
5.  **Pacotes Nix**: Deixe **vazio**.
6.  **Pacotes APT**: Deixe **vazio**.

### E se não funcionar de primeira?
Se o site não abrir, é porque o Nixpacks não "adivinhou" que é um site estático. Nesse caso, use a **Alternativa infalível**:

### Alternativa: Dockerfile (Recomendada para sites estáticos)
No Easypanel, o **Dockerfile** é o método mais garantido para arquivos HTML simples:

1.  No seu VS Code, crie um arquivo chamado `Dockerfile` (sem extensão) na raiz com este código:
    ```dockerfile
    FROM nginx:alpine
    COPY . /usr/share/nginx/html
    ```
2.  Dê `git add .`, `git commit` e `git push`.
3.  No Easypanel, mude o **Build Method** de Nixpacks para **Dockerfile**.
4.  Clique em **Salvar** e **Deploy**.

> [!TIP]
> O Dockerfile acima pega todos os seus arquivos (incluindo as pastas de jogos geradas) e os coloca dentro de um servidor Nginx super rápido e estável.

---

## 🔗 Passo 5: Configurar Domínio e SSL

1.  No menu **Domains** do Easypanel:
2.  Adicione `ONDEVAIPASSARFUTEBOLHOJE.COM.BR`.
3.  Adicione `www.ONDEVAIPASSARFUTEBOLHOJE.COM.BR`.
4.  O Easypanel vai gerar o certificado **SSL (HTTPS)** automaticamente via Let's Encrypt.

---

## 🔄 Fluxo de Atualização Diária

Sempre que você quiser atualizar os placares ou adicionar jogos:

1.  No seu computador, edite `data/matches.json`.
2.  No terminal local, rode:
    ```powershell
    .venv\Scripts\python spiders/generate_match_pages.py
    ```
3.  Dê o commit e push:
    ```powershell
    git add .
    git commit -m "Atualização de jogos do dia"
    git push
    ```
4.  O **Easypanel** vai detectar o push e o site estará atualizado em segundos!

---

## ⚠️ Dica para URLs Amigáveis no Easypanel

Para que os links como `/paulistao26/18-01-2026/jogo/` funcionem sem erro 404, o Easypanel (que usa Nginx por baixo) precisa ser configurado. 

No menu **General** ou seguindo a regra de redirecionamento do painel, certifique-se de que ele está servindo arquivos `.html` automaticamente. Se ele pedir um arquivo de configuração customizado, use:

```nginx
location / {
    try_files $uri $uri/ $uri.html =404;
}
```

---

© 2026 Onde Vai Passar Futebol Hoje
