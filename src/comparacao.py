import json

import pandas as pd


COLUNAS_COMPARAVEIS = [
	"id_cliente",
	"status",
	"valor_total",
	"atualizado_em",
]


def validar_colunas_comparacao(
	origem: pd.DataFrame,
	destino: pd.DataFrame,
) -> None:
	"""Valida as colunas necessarias para comparar os estados."""
	colunas_necessarias = {"id_pedido", *COLUNAS_COMPARAVEIS}

	for nome, dados in (("origem", origem), ("destino", destino)):
		faltantes = colunas_necessarias - set(dados.columns)
		if faltantes:
			raise ValueError(
				f"Colunas obrigatorias ausentes em {nome}: {sorted(faltantes)}"
			)


def obter_ids_duplicados(dados: pd.DataFrame) -> set:
	"""Retorna os IDs que aparecem mais de uma vez no DataFrame."""
	return set(
		dados.loc[dados["id_pedido"].duplicated(keep=False), "id_pedido"]
	)


def _valores_diferentes(valor_origem, valor_destino) -> bool:
	"""Compara valores considerando dois valores ausentes como iguais."""
	ambos_ausentes = pd.isna(valor_origem) and pd.isna(valor_destino)
	if ambos_ausentes:
		return False

	if pd.isna(valor_origem) or pd.isna(valor_destino):
		return True

	return valor_origem != valor_destino


def comparar_campos(linha_origem: pd.Series, linha_destino: pd.Series) -> dict:
	"""Retorna os campos com valores diferentes entre dois pedidos."""
	diferencas = {}

	for coluna in COLUNAS_COMPARAVEIS:
		valor_origem = linha_origem[coluna]
		valor_destino = linha_destino[coluna]

		if _valores_diferentes(valor_origem, valor_destino):
			diferencas[coluna] = {
				"origem": str(valor_origem),
				"destino": str(valor_destino),
			}

	return diferencas


def _criar_divergencia(
	id_pedido,
	tipo: str,
	valores_origem=None,
	valores_destino=None,
	campos: list[str] | None = None,
) -> dict:
	"""Monta uma linha padronizada do relatório de divergências."""
	return {
		"id_pedido": id_pedido,
		"tipo_divergencia": tipo,
		"campos_divergentes": ",".join(campos or []),
		"valor_origem": json.dumps(valores_origem, ensure_ascii=False, default=str),
		"valor_destino": json.dumps(
			valores_destino, ensure_ascii=False, default=str
		),
	}


def comparar_estados(
	origem: pd.DataFrame,
	destino: pd.DataFrame,
) -> pd.DataFrame:
	"""Compara a origem reconstruida com o destino, uma linha por pedido."""
	validar_colunas_comparacao(origem, destino)

	ids_origem = set(origem["id_pedido"])
	ids_destino = set(destino["id_pedido"])
	ids_duplicados_destino = obter_ids_duplicados(destino)
	divergencias = []


	for id_pedido in sorted(ids_origem - ids_destino):
		divergencias.append(
			_criar_divergencia(
				id_pedido,
				"AUSENTE_NO_DESTINO",
				valores_origem={"existe": True},
				valores_destino={"existe": False},
			)
		)

	for id_pedido in sorted(ids_destino - ids_origem):
		linhas_destino = destino[destino["id_pedido"] == id_pedido]
		divergencias.append(
			_criar_divergencia(
				id_pedido,
				"INDEVIDO_NO_DESTINO",
				valores_origem={"existe": False},
				valores_destino={"quantidade": len(linhas_destino)},
			)
		)

	for id_pedido in sorted(ids_duplicados_destino & ids_origem):
		linhas_destino = destino[destino["id_pedido"] == id_pedido]
		divergencias.append(
			_criar_divergencia(
				id_pedido,
				"DUPLICADO_NO_DESTINO",
				valores_origem={"existe": True},
				valores_destino={"quantidade": len(linhas_destino)},
			)
		)

	ids_para_comparar = (ids_origem & ids_destino) - ids_duplicados_destino
	origem_indexada = origem.set_index("id_pedido")
	destino_indexado = destino.set_index("id_pedido")

	for id_pedido in sorted(ids_para_comparar):
		diferencas = comparar_campos(
			origem_indexada.loc[id_pedido], destino_indexado.loc[id_pedido]
		)
		if diferencas:
			tipo = (
				"MULTIPLOS_CAMPOS_DIVERGENTES"
				if len(diferencas) > 1
				else f"{next(iter(diferencas)).upper()}_DIVERGENTE"
			)
			divergencias.append(
				_criar_divergencia(
					id_pedido,
					tipo,
					valores_origem={
						campo: valores["origem"]
						for campo, valores in diferencas.items()
					},
					valores_destino={
						campo: valores["destino"]
						for campo, valores in diferencas.items()
					},
					campos=list(diferencas),
				)
			)

	return pd.DataFrame(
		divergencias,
		columns=[
			"id_pedido",
			"tipo_divergencia",
			"campos_divergentes",
			"valor_origem",
			"valor_destino",
		],
	).sort_values("id_pedido").reset_index(drop=True)
