# Deploy do ByteShift

Backend e frontend são publicados em serviços separados — o backend precisa rodar Python, o frontend é só arquivo estático.

## 1. Backend (Render)

Render tem plano gratuito e detecta projetos Python automaticamente. Railway funciona de forma bem parecida, se preferir.

1. Suba o repositório pro GitHub (se ainda não estiver lá)
2. Em [render.com](https://render.com), **New +** → **Web Service** → conecte o repositório
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free
4. Deploy. Ao terminar, você recebe uma URL tipo `https://byteshift-api.onrender.com`

**Importante — CORS**: depois do deploy do *frontend* (passo 2), volte em `backend/app/main.py` e adicione a URL de produção do frontend na lista `origins`:

```python
origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://SEU-FRONTEND-AQUI.vercel.app",  # adicionar depois do passo 2
]
```

Commit e o Render redeploya sozinho (deploy automático a cada push, por padrão).

> No plano gratuito do Render, o serviço "dorme" depois de um tempo sem uso e demora uns 30-50s pra acordar na primeira requisição — normal, não é bug.

## 2. Frontend (Vercel, Netlify ou GitHub Pages)

Qualquer um dos três funciona bem pra arquivo estático puro. Vercel é o mais direto:

1. Em [vercel.com](https://vercel.com), **Add New** → **Project** → conecte o repositório
2. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Other (não tem build step, é HTML/CSS/JS puro)
   - **Build Command**: deixe vazio
   - **Output Directory**: `.`
3. Deploy. Você recebe uma URL tipo `https://byteshift.vercel.app`

**GitHub Pages** como alternativa: em Settings → Pages do repositório, aponte pra pasta `frontend/` na branch principal.

## 3. Conectar os dois

Depois que o backend estiver publicado:

1. Abra `frontend/js/config.js`
2. Troque `PRODUCTION_API_URL` pela URL real do backend (ex: `https://byteshift-api.onrender.com`)
3. Commit — o Vercel/Netlify redeploya sozinho

Depois que o frontend estiver publicado, volte no passo 1 (CORS) e adicione a URL dele.

## 4. Verificação pós-deploy

- `https://SEU-BACKEND/docs` → Swagger deve carregar e listar todas as rotas (`/convert/*`, `/units`, `/convert/context/*`)
- `https://SEU-FRONTEND` → os 4 cards devem carregar as unidades (se ficarem vazios, é quase sempre CORS — confira a lista `origins` no backend)
- Teste uma conversão de cada gênero e um cenário contextual pra confirmar que o frontend está de fato falando com o backend publicado, não com localhost

## 5. Atualizar o README

Depois de tudo no ar, preencha as 3 linhas em branco no final do `README.md`:

```
**API em produção**: https://SEU-BACKEND/
**Swagger público**: https://SEU-BACKEND/docs
**Frontend em produção**: https://SEU-FRONTEND/
```
