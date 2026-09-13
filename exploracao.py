import pandas as pd

origem = pd.read_csv("dados/pedidos_origem.csv")
destino = pd.read_csv("dados/pedidos_destino.csv")

print("=== DIMENSÕES ===")
print("Origem:", origem.shape)
print("Destino:", destino.shape)

print("\n=== COLUNAS ===")
print("Origem:", list(origem.columns))
print("Destino:", list(destino.columns))

print("\n=== TIPOS ===")
print(origem.dtypes)
print(destino.dtypes)

print("\n=== PRIMEIRAS LINHAS ===")
print(origem.head())
print(destino.head())

print("\n=== VALORES VAZIOS ===")
print("Origem:")
print(origem.isna().sum())

print("\nDestino:")
print(destino.isna().sum())

print("\n=== EVENTOS COM VALOR_TOTAL VAZIO ===")
eventos_valor_vazio = origem[origem["valor_total"].isna()]
print(eventos_valor_vazio)

print("\n=== OPERAÇÕES DA ORIGEM ===")
print(origem["operacao"].value_counts())

print("\n=== STATUS DA ORIGEM ===")
print(origem["status"].value_counts())

print("\n=== STATUS DO DESTINO ===")
print(destino["status"].value_counts())

print("\n=== IDS DUPLICADOS NO DESTINO ===")
ids_repetidos = destino[
    destino["id_pedido"].duplicated(keep=False)
].sort_values("id_pedido")
ids_duplicados_destino = (
    ids_repetidos["id_pedido"].drop_duplicates().tolist()
)
print("Lista de IDs duplicados:", ids_duplicados_destino)

print("\n=== IDS UNICOS NO DESTINO ===")
ids_unicos_destino = destino["id_pedido"].nunique()
print("Quantidade de IDs únicos no destino:", ids_unicos_destino)

print(ids_repetidos)

print("\n=== IDS UNICOS NA ORIGEM ===")
ids_unicos_origem = origem["id_pedido"].nunique()
print("Quantidade de IDs únicos na origem:", ids_unicos_origem)

print("\n=== QUANTIDADE DE EVENTOS POR PEDIDO NA ORIGEM ===")
eventos_por_pedido = origem["id_pedido"].value_counts()

print(eventos_por_pedido.describe())

print("\nPedidos com mais de um evento:")
print(eventos_por_pedido[eventos_por_pedido > 1].head(20))