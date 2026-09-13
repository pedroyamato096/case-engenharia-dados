from pathlib import Path

import pandas as pd


def ler_csv(caminho: str | Path, colunas_obrigatorias: list[str]) -> pd.DataFrame:
	"""Le um CSV e valida sua existencia e estrutura minima."""
	caminho = Path(caminho)

	if not caminho.is_file():
		raise FileNotFoundError(f"Arquivo nao encontrado: {caminho}")

	try:
		dados = pd.read_csv(caminho)
	except pd.errors.EmptyDataError as erro:
		raise ValueError(f"Arquivo CSV vazio: {caminho}") from erro
	except pd.errors.ParserError as erro:
		raise ValueError(f"Arquivo CSV invalido: {caminho}") from erro

	colunas_faltantes = [
		coluna for coluna in colunas_obrigatorias if coluna not in dados.columns
	]
	if colunas_faltantes:
		raise ValueError(
			f"Colunas obrigatorias ausentes em {caminho}: {colunas_faltantes}"
		)

	if dados.empty:
		raise ValueError(f"Arquivo CSV sem registros: {caminho}")

	return dados
