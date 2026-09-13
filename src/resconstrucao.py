import pandas as pd


COLUNAS_OBRIGATORIAS = {
    "id_pedido",
    "status",
    "valor_total",
    "atualizado_em",
    "operacao",
}


def validar_eventos(dados: pd.DataFrame) -> None:
    """Valida as colunas necessarias para reconstruir os pedidos."""
    colunas_faltantes = COLUNAS_OBRIGATORIAS - set(dados.columns)
    if colunas_faltantes:
        raise ValueError(
            f"Colunas obrigatorias ausentes: {sorted(colunas_faltantes)}"
        )


def ordenar_eventos(dados: pd.DataFrame) -> pd.DataFrame:
    """Ordena eventos por pedido, data e ordem original do arquivo."""
    dados_ordenados = dados.copy()
    dados_ordenados["_ordem_original"] = range(len(dados_ordenados))

    return dados_ordenados.sort_values(
        by=["id_pedido", "atualizado_em", "_ordem_original"],
        kind="stable",
    )


def selecionar_ultimo_evento(dados: pd.DataFrame) -> pd.DataFrame:
    """Seleciona o evento mais recente de cada pedido."""
    dados_ordenados = ordenar_eventos(dados)
    ultimos_eventos = dados_ordenados.groupby(
        "id_pedido", as_index=False, sort=False
    ).tail(1)

    return ultimos_eventos.sort_values("id_pedido").reset_index(drop=True)


def separar_pedidos_excluidos(
    ultimos_eventos: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa pedidos ativos dos pedidos cujo ultimo evento e uma exclusao."""
    pedidos_excluidos = ultimos_eventos[
        ultimos_eventos["operacao"] == "D"
    ].copy()
    pedidos_ativos = ultimos_eventos[
        ultimos_eventos["operacao"] != "D"
    ].copy()

    return (
        pedidos_ativos.drop(columns="operacao").reset_index(drop=True),
        pedidos_excluidos.drop(columns="operacao").reset_index(drop=True),
    )


def reconstruir_estado_atual(
    dados: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Reconstrói o estado ativo e separa os pedidos excluídos."""
    validar_eventos(dados)
    ultimos_eventos = selecionar_ultimo_evento(dados)
    return separar_pedidos_excluidos(ultimos_eventos)