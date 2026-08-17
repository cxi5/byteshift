"""
Ponto de entrada da aplicação FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import context, convert, units

app = FastAPI(
    title="ByteShift API",
    description="Conversor de unidades técnicas (armazenamento, velocidade, rede, capacidade de dispositivos).",
    version="1.0.0",
)

# CORS: localhost (dev) + frontend de produção (Vercel)
origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://byteshift-seven.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=False de propósito: essa API não usa cookies nem
    # sessão, então não há motivo pra permitir requisições cross-origin
    # com credenciais — isso só ampliaria a superfície de ataque à toa.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(convert.router)
app.include_router(units.router)
app.include_router(context.router)


@app.get("/")
def hello_world():
    return {"message": "ByteShift API no ar"}
