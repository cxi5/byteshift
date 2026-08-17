# Backend — ByteShift

API em FastAPI responsável pela lógica de conversão de unidades técnicas.

## Estrutura

```
app/
├── main.py              # ponto de entrada, CORS, registro de rotas
├── core/
│   ├── constants.py     # tabelas de unidades por gênero
│   ├── conversion_engine.py  # motor de conversão compartilhado
│   ├── exceptions.py    # erros de negócio centralizados
│   └── validators.py    # validação e arredondamento
├── services/            # 1 arquivo por gênero + context_service.py
├── routers/             # convert.py, units.py, context.py
├── schemas/             # modelos Pydantic (request/response)
└── tests/               # 63 testes automatizados
```

## Como rodar

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API em `http://localhost:8000`. Documentação interativa em `http://localhost:8000/docs`.

## Testes

```bash
pytest --cov=app --cov-report=term-missing
```

## Produção

- **API**: https://byteshift-t5oi.onrender.com/
- **Swagger**: https://byteshift-t5oi.onrender.com/docs
