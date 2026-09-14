import pandas as pd


def normalizar_status(status: pd.Series) -> pd.Series:
	"""Padroniza status removendo espacos e diferencias de maiusculas."""
	return status.astype("string").str.strip().str.upper()


def normalizar_valores(valor_total: pd.Series) -> pd.Series:
	"""Converte valores para numero sem preencher valores ausentes."""
	return pd.to_numeric(valor_total, errors="coerce")


def normalizar_datas(
	atualizado_em: pd.Series,
	fuso_horario_sem_fuso: str = "America/Sao_Paulo",
) -> pd.Series:
	"""Converte datas para UTC e assume fuso local quando ele nao foi informado."""
	datas = pd.to_datetime(atualizado_em, errors="coerce")

	if datas.dt.tz is None:
		datas = datas.dt.tz_localize(fuso_horario_sem_fuso)

	return datas.dt.tz_convert("UTC")


def normalizar_dataframe(
	dados: pd.DataFrame,
	tem_operacao: bool = False,
	fuso_horario_sem_fuso: str = "America/Sao_Paulo",
) -> pd.DataFrame:
	"""Retorna uma copia com os campos conhecidos normalizados."""
	dados_normalizados = dados.copy()

	if "status" in dados_normalizados.columns:
		dados_normalizados["status"] = normalizar_status(
			dados_normalizados["status"]
		)

	if "valor_total" in dados_normalizados.columns:
		dados_normalizados["valor_total"] = normalizar_valores(
			dados_normalizados["valor_total"]
		)

	if "atualizado_em" in dados_normalizados.columns:
		dados_normalizados["atualizado_em"] = normalizar_datas(
			dados_normalizados["atualizado_em"],
			fuso_horario_sem_fuso,
		)

	if tem_operacao and "operacao" in dados_normalizados.columns:
		dados_normalizados["operacao"] = (
			dados_normalizados["operacao"].astype("string").str.strip().str.upper()
		)

	return dados_normalizados
