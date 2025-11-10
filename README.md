# Classificador de Emails - MVP

**Aplicação web para classificação automática de emails e geração de respostas.**

## 🎯 O Problema

Empresas recebem muitos emails diariamente. Muitos são improdutivos (felicitações, agradecimentos) que sobrecarregam a equipe, enquanto emails produtivos (solicitações, dúvidas) precisam de atenção imediata.

**Esta solução automatiza a classificação e gera respostas adequadas.**

## ✨ Funcionalidades

- ✅ Classificação automática (Produtivo vs Improdutivo)
- ✅ Geração de respostas automáticas via IA
- ✅ Upload de arquivos (.txt e .pdf)
- ✅ Interface web limpa e profissional
- ✅ API REST para integração

## 🚀 Como Rodar

### 1. Instalar dependências

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` e adicione sua chave da OpenAI:
```
OPENAI_API_KEY=sua-chave-aqui
```

### 3. Executar

```bash
python run.py
```

Acesse: **http://localhost:5001**

## 📁 Estrutura do Projeto

```
estagio/
├── backend/           # Flask app
├── frontend/          # HTML/CSS/JS
├── src/              # Lógica de classificação e processamento
│   ├── classifiers/  # Classificador de emails
│   ├── generators/   # Gerador de respostas
│   └── processors/   # Processamento de texto/PDF
├── tests/            # Testes
├── examples/         # Emails de exemplo
└── run.py           # Script principal
```

## 🧪 Testar

Exemplos prontos em `examples/`:
- `email_produtivo.txt` - Email que precisa de atenção
- `email_improdutivo.txt` - Email genérico

## 📡 API REST

**POST /api/classify**

```json
{
  "text": "Texto do email aqui"
}
```

**Response:**
```json
{
  "category": "Produtivo",
  "confidence": 0.95,
  "suggested_response": "Resposta gerada automaticamente..."
}
```

## 🌐 Deploy

### Render
1. Conecte seu repositório GitHub
2. Configure `OPENAI_API_KEY` nas variáveis de ambiente
3. Deploy automático via `render.yaml`

### Heroku
```bash
heroku create
heroku config:set OPENAI_API_KEY=sua-chave
git push heroku main
```

## 🛠️ Tecnologias

- **Backend**: Flask + OpenAI API
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Processamento**: PyPDF2
- **Deploy**: Render/Heroku/Vercel

## 📝 Licença

Projeto desenvolvido para processo seletivo.
