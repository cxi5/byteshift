"""
Fatores de conversão e unidades-base, isolados por gênero.

Regra de ouro: nenhuma função genérica "converte tudo" usa essas tabelas.
Cada gênero só é lido pelo seu próprio serviço (ver app/services/).
"""

from dataclasses import dataclass
from typing import Literal

UnitSystem = Literal["base", "decimal", "binary"]


@dataclass(frozen=True)
class UnitDefinition:
    key: str                # identificador usado na API (ex: "gigabyte")
    symbol: str              # símbolo de exibição (ex: "GB")
    label: str               # nome legível (ex: "Gigabyte")
    factor_to_base: float    # fator de multiplicação até a unidade-base do gênero
    system: UnitSystem       # "base" | "decimal" | "binary"


def _build_table(raw: dict[str, tuple[str, str, float, UnitSystem]]) -> dict[str, UnitDefinition]:
    """
    Monta uma tabela de unidades a partir de um dicionário mais enxuto,
    onde a chave já É o identificador da unidade.

    Isso existe pra eliminar um bug silencioso possível: antes, o `key`
    de cada UnitDefinition era digitado duas vezes (uma como chave do
    dicionário, outra como primeiro argumento). Se algum dia esses dois
    valores fossem digitados de forma diferente por engano, a tabela
    interna continuaria funcionando normalmente, mas o endpoint /units
    reportaria uma chave errada pro frontend — um bug que passaria
    despercebido em qualquer teste que só olhasse os fatores de conversão.
    Agora o `key` é sempre derivado da própria chave do dicionário, então
    os dois nunca podem divergir.
    """
    return {
        key: UnitDefinition(key=key, symbol=symbol, label=label, factor_to_base=factor, system=system)
        for key, (symbol, label, factor, system) in raw.items()
    }


# Armazenamento — unidade-base interna: bit
STORAGE_BASE_UNIT = "bit"

STORAGE_UNITS: dict[str, UnitDefinition] = _build_table({
    # Unidades base (não seguem prefixo decimal nem binário)
    "bit": ("b", "Bit", 1, "base"),
    "byte": ("B", "Byte", 8, "base"),

    # Decimais (SI, potências de 1000) — bits
    "kilobit": ("kb", "Kilobit", 1_000, "decimal"),
    "megabit": ("Mb", "Megabit", 1_000**2, "decimal"),
    "gigabit": ("Gb", "Gigabit", 1_000**3, "decimal"),
    "terabit": ("Tb", "Terabit", 1_000**4, "decimal"),

    # Decimais (SI, potências de 1000) — bytes
    "kilobyte": ("KB", "Kilobyte", 8 * 1_000, "decimal"),
    "megabyte": ("MB", "Megabyte", 8 * 1_000**2, "decimal"),
    "gigabyte": ("GB", "Gigabyte", 8 * 1_000**3, "decimal"),
    "terabyte": ("TB", "Terabyte", 8 * 1_000**4, "decimal"),
    "petabyte": ("PB", "Petabyte", 8 * 1_000**5, "decimal"),

    # Binários (IEC, potências de 1024) — apenas bytes (uso real de mercado)
    "kibibyte": ("KiB", "Kibibyte", 8 * 1024, "binary"),
    "mebibyte": ("MiB", "Mebibyte", 8 * 1024**2, "binary"),
    "gibibyte": ("GiB", "Gibibyte", 8 * 1024**3, "binary"),
    "tebibyte": ("TiB", "Tebibyte", 8 * 1024**4, "binary"),
    "pebibyte": ("PiB", "Pebibyte", 8 * 1024**5, "binary"),
})


# Velocidade (transferência de arquivos) — unidade-base interna: byte/s
SPEED_BASE_UNIT = "byte_per_second"

SPEED_UNITS: dict[str, UnitDefinition] = _build_table({
    "byte_per_second": ("B/s", "Byte por segundo", 1, "base"),

    # Decimais
    "kilobyte_per_second": ("KB/s", "Kilobyte por segundo", 1_000, "decimal"),
    "megabyte_per_second": ("MB/s", "Megabyte por segundo", 1_000**2, "decimal"),
    "gigabyte_per_second": ("GB/s", "Gigabyte por segundo", 1_000**3, "decimal"),

    # Binários (o que Windows/macOS costumam exibir de fato)
    "kibibyte_per_second": ("KiB/s", "Kibibyte por segundo", 1024, "binary"),
    "mebibyte_per_second": ("MiB/s", "Mebibyte por segundo", 1024**2, "binary"),
    "gibibyte_per_second": ("GiB/s", "Gibibyte por segundo", 1024**3, "binary"),
})


# Rede (banda de internet) — unidade-base interna: bit/s
# Padrão da indústria: sempre decimal (ISPs, datasheets, roteadores).
# Não existe versão binária de uso real aqui — por isso não há tabela binária.
NETWORK_BASE_UNIT = "bit_per_second"

NETWORK_UNITS: dict[str, UnitDefinition] = _build_table({
    "bit_per_second": ("bps", "Bit por segundo", 1, "base"),
    "kilobit_per_second": ("kbps", "Kilobit por segundo", 1_000, "decimal"),
    "megabit_per_second": ("Mbps", "Megabit por segundo", 1_000**2, "decimal"),
    "gigabit_per_second": ("Gbps", "Gigabit por segundo", 1_000**3, "decimal"),
})


# Capacidade de dispositivos — lógica própria e contextual.
# Converte capacidade ANUNCIADA (decimal, do fabricante) para capacidade
# REAL exibida pelo sistema operacional (binária). Unidade-base: byte.
# Nunca cruza com a tabela de Armazenamento, mesmo usando bytes também —
# tabelas isoladas por design, mesmo repetindo fatores.
DEVICE_CAPACITY_BASE_UNIT = "byte"

DEVICE_CAPACITY_ADVERTISED_UNITS: dict[str, UnitDefinition] = _build_table({
    # O que vem escrito na caixa/anúncio do produto — sempre decimal
    "kilobyte": ("KB", "Kilobyte (anunciado)", 1_000, "decimal"),
    "megabyte": ("MB", "Megabyte (anunciado)", 1_000**2, "decimal"),
    "gigabyte": ("GB", "Gigabyte (anunciado)", 1_000**3, "decimal"),
    "terabyte": ("TB", "Terabyte (anunciado)", 1_000**4, "decimal"),
})

DEVICE_CAPACITY_REAL_UNITS: dict[str, UnitDefinition] = _build_table({
    # O que o sistema operacional exibe de fato — sempre binário
    "kibibyte": ("KiB", "Kibibyte (real)", 1024, "binary"),
    "mebibyte": ("MiB", "Mebibyte (real)", 1024**2, "binary"),
    "gibibyte": ("GiB", "Gibibyte (real)", 1024**3, "binary"),
    "tebibyte": ("TiB", "Tebibyte (real)", 1024**4, "binary"),
})


# Regras de integridade (Fase 2.3)
DEFAULT_ROUNDING_PRECISION = 6  # casas decimais aplicadas a qualquer resultado de conversão
