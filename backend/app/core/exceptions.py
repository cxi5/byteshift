"""
Exceções de negócio da camada de conversão, centralizadas num só lugar.

Antes, cada serviço declarava sua própria classe InvalidUnitError com o
mesmo nome, obrigando as rotas a importar e apelidar quatro classes
diferentes. Agora existe uma única fonte: os serviços reexportam essas
classes (então quem já importava de app.services.*_service continua
funcionando), e as rotas podem tratar qualquer erro de conversão
capturando só a classe-base ConversionError.
"""


class ConversionError(ValueError):
    """Classe-base de qualquer erro de negócio da camada de conversão."""


class InvalidUnitError(ConversionError):
    """A unidade pedida não existe na tabela do gênero consultado."""


class InvalidValueError(ConversionError):
    """O valor de entrada não é um número finito e válido (ex: texto, NaN, infinito)."""


class NegativeValueError(InvalidValueError):
    """O valor de entrada é negativo — conversões não aceitam números negativos."""
