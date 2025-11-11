# 🎬 Roteiro do Vídeo Demonstrativo
## Classificador de Emails com IA

**Duração: 3-5 minutos**

---

## 📋 **Estrutura do Vídeo**

### 1️⃣ INTRODUÇÃO (30 segundos)
**O QUE FALAR:**
- "Olá! Sou [Seu Nome] e vou apresentar minha solução para o desafio de estágio"
- "Criei um classificador automático de emails usando IA"
- "Vou mostrar o problema, a solução e uma demonstração ao vivo"

**O QUE MOSTRAR:**
- Tela inicial da aplicação
- URL do projeto no Railway

---

### 2️⃣ O PROBLEMA (45 segundos)
**O QUE FALAR:**
- "Empresas recebem centenas de emails por dia"
- "Muitos são improdutivos: felicitações, agradecimentos genéricos"
- "Isso sobrecarrega a equipe de atendimento"
- "Emails produtivos - solicitações e problemas - precisam de atenção imediata"
- "A solução: automatizar essa classificação"

**O QUE MOSTRAR:**
- Slides simples OU
- Exemplos de emails na tela (abra os arquivos examples/)

---

### 3️⃣ A SOLUÇÃO (1 minuto)
**O QUE FALAR:**
- "Criei uma aplicação web que classifica emails automaticamente"
- "Backend em Python com Flask"
- "Integração com OpenAI GPT-3.5 para classificação inteligente"
- "Interface web simples e intuitiva"
- "Suporta texto direto e upload de arquivos (.txt e .pdf)"
- "Gera respostas automáticas contextuais"

**O QUE MOSTRAR:**
- Arquitetura (pode usar um diagrama simples OU mostrar a estrutura de pastas)
- Falar das tecnologias: Flask, OpenAI API, PyPDF2, gunicorn

---

### 4️⃣ DEMONSTRAÇÃO AO VIVO (2 minutos) ⭐ **MAIS IMPORTANTE**
**DEMO 1: Email Produtivo (via texto)**
1. Acesse: https://web-production-f81ca.up.railway.app/
2. Clique na aba "Inserir Texto"
3. Cole este email:
```
Prezados,

Preciso de ajuda urgente com um problema que estou enfrentando no sistema. Quando tento fazer login, recebo uma mensagem de erro dizendo "Credenciais inválidas", mesmo utilizando as mesmas credenciais que funcionavam anteriormente.

Já tentei:
- Limpar o cache do navegador
- Verificar se as credenciais estão corretas
- Tentar em outro navegador

O problema começou ontem e está impedindo meu trabalho. Por favor, preciso de suporte técnico o quanto antes.

Atenciosamente,
João Silva
```
4. Clique em "Classificar Email"
5. **EXPLIQUE O RESULTADO:**
   - "Veja: classificou como PRODUTIVO com 90% de confiança"
   - "E gerou uma resposta profissional automática"

**DEMO 2: Email Improdutivo (via upload)**
1. Clique na aba "Upload de Arquivo"
2. Faça upload do arquivo `email_improdutivo.txt`
3. Clique em "Classificar Email"
4. **EXPLIQUE O RESULTADO:**
   - "Este é um email de felicitações - IMPRODUTIVO"
   - "A IA identificou corretamente e gerou uma resposta curta e cortês"

**MOSTRE TAMBÉM:**
- A velocidade da resposta
- A interface limpa e profissional
- Opcional: abra o DevTools e mostre a chamada da API

---

### 5️⃣ DIFERENCIAIS TÉCNICOS (45 segundos)
**O QUE FALAR:**
- "A aplicação tem fallback: funciona mesmo sem a API da OpenAI"
- "Deploy em produção no Railway com Docker"
- "Código versionado no GitHub com histórico de commits profissional"
- "Testes unitários implementados"
- "API REST documentada para integração"

**O QUE MOSTRAR:**
- Repositório GitHub: https://github.com/ResetToBasics/AutoU
- Mostrar os commits (11 commits organizados)
- Opcional: mostrar estrutura do código

---

### 6️⃣ CONCLUSÃO (30 segundos)
**O QUE FALAR:**
- "Esta solução resolve um problema real: economiza tempo da equipe"
- "Emails improdutivos recebem resposta automática"
- "Emails produtivos são priorizados para atendimento humano"
- "O resultado: equipe mais produtiva e clientes mais satisfeitos"
- "Obrigado pela atenção!"

**O QUE MOSTRAR:**
- Tela final com a aplicação rodando
- Seus contatos (GitHub, LinkedIn, email)

---

## 🎯 **DICAS IMPORTANTES**

### ✅ **FAÇA:**
- Fale de forma clara e pausada
- Mostre confiança e domínio do projeto
- Explique o PORQUÊ, não só o QUE
- Mostre a aplicação funcionando DE VERDADE
- Seja objetivo: 3-5 minutos é ideal

### ❌ **NÃO FAÇA:**
- Não use jargão técnico demais
- Não leia um texto decorado
- Não foque só em tecnologia (fale do problema que resolve!)
- Não grave com áudio ruim ou fundo bagunçado
- Não ultrapasse 5 minutos

---

## 🎥 **FERRAMENTAS RECOMENDADAS**

### Gravação de Tela:
- **Mac**: QuickTime (CMD+Shift+5) ou OBS Studio
- **Windows**: Xbox Game Bar (Win+G) ou OBS Studio
- **Linux**: OBS Studio ou SimpleScreenRecorder

### Edição (opcional):
- iMovie (Mac)
- DaVinci Resolve (gratuito, multiplataforma)
- Clipchamp (Windows)

### Upload:
- YouTube (não listado ou público)
- Loom
- Google Drive

---

## 📝 **CHECKLIST PRÉ-GRAVAÇÃO**

- [ ] Aplicação rodando no Railway
- [ ] Arquivos de exemplo prontos
- [ ] Roteiro revisado
- [ ] Ambiente organizado (desktop limpo)
- [ ] Microfone testado
- [ ] Navegador em modo anônimo (sem extensões aparecendo)
- [ ] GitHub aberto em outra aba
- [ ] Água por perto (não fale com a boca seca!)

---

## 🎬 **BOA SORTE!**

Lembre-se: eles querem ver:
1. Que você entendeu o problema
2. Que criou uma solução funcional
3. Que sabe explicar bem
4. Que tem visão de produto, não só código

**Você consegue! 🚀**
