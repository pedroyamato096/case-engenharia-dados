from pathlib import Path

from src.comparacao import comparar_estados
from src.leitura import ler_csv
from src.normalizacao import normalizar_dataframe
from src.resconstrucao import reconstruir_estado_atual


COLUNAS_ORIGEM = [
    "id_pedido",
    "status",
    "valor_total",
    "atualizado_em",
    "operacao",
]
COLUNAS_DESTINO = ["id_pedido", "id_cliente", "status", "valor_total", "atualizado_em"]


PASTA_PROJETO = Path(__file__).parent
PASTA_DADOS = PASTA_PROJETO / "dados"
PASTA_SAIDA = PASTA_PROJETO / "saida"


def main():
    origem = ler_csv(PASTA_DADOS / "pedidos_origem.csv", COLUNAS_ORIGEM)
    destino = ler_csv(PASTA_DADOS / "pedidos_destino.csv", COLUNAS_DESTINO)

    origem = normalizar_dataframe(
        origem,
        tem_operacao=True,
        fuso_horario_sem_fuso="America/Sao_Paulo",
    )
    destino = normalizar_dataframe(
        destino,
        fuso_horario_sem_fuso="UTC",
    )

    origem_atual, pedidos_excluidos = reconstruir_estado_atual(origem)
    divergencias = comparar_estados(origem_atual, destino)

    PASTA_SAIDA.mkdir(exist_ok=True)
    divergencias.to_csv(PASTA_SAIDA / "relatorio_divergencias.csv", index=False)

    print(f"Pedidos ativos reconstruídos: {len(origem_atual)}")
    print(f"Pedidos excluídos: {len(pedidos_excluidos)}")
    print(f"Pedidos divergentes: {divergencias['id_pedido'].nunique()}")
    print("\nDivergências por tipo:")
    print(divergencias["tipo_divergencia"].value_counts().sort_index())
    print(f"\nFaturamento na origem: R$ {origem_atual['valor_total'].sum():,.2f}")
    print(f"Faturamento no destino: R$ {destino['valor_total'].sum():,.2f}")
    print(
        "Impacto financeiro (origem - destino): "
        f"R$ {origem_atual['valor_total'].sum() - destino['valor_total'].sum():,.2f}"
    )
    print(f"Relatório salvo em: {PASTA_SAIDA / 'relatorio_divergencias.csv'}")


if __name__ == "__main__":
    main()