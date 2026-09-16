# Reconciliação de pedidos

Solução do case técnico de Engenharia de Dados. O projeto reconstrói o estado atual dos pedidos a partir do log de eventos, compara o resultado com a tabela analítica e gera um relatório de divergências.

## Tecnologias

- Python 3.12 ou superior
- pandas para leitura, normalização e comparação dos CSVs
- Git e GitHub para versionamento e entrega

Não há necessidade de banco de dados, Docker ou ferramenta de orquestração para o volume e o escopo deste case. A solução pode ser executada localmente do início ao fim.

## Pré-requisitos

- Python 3.12 ou superior instalado e disponível no terminal como `python` ou `py`
- Git instalado para clonar o repositório

## Instalação no Windows

Clone o repositório e entre na pasta do projeto:

```powershell
git clone URL_DO_REPOSITORIO
cd NOME_DO_REPOSITORIO
```

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se o PowerShell bloquear a ativação do ambiente, execute uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Instalação no macOS ou Linux

```bash
git clone URL_DO_REPOSITORIO
cd NOME_DO_REPOSITORIO
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Estrutura

```text
.
|-- dados/       # CSVs recebidos para o case
|-- saida/       # relatório gerado (CSV ignorado pelo Git)
|-- src/         # leitura, normalização, reconstrução e comparação
|-- main.py      # ponto de entrada
|-- requirements.txt
|-- RESUMO.md
|-- DECISOES.md
`-- CASE_Engenharia_de_Dados.md
```

Os arquivos `dados/pedidos_origem.csv` e `dados/pedidos_destino.csv` já acompanham o repositório. Para usar outros arquivos, substitua-os mantendo esses nomes e as colunas esperadas pelo case.

## Execução

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

macOS/Linux:

```bash
source .venv/bin/activate
python main.py
```

O relatório será salvo em `saida/relatorio_divergencias.csv`. A pasta `saida/` permanece no Git por meio de `.gitkeep`, mas os relatórios gerados são ignorados para evitar alterações locais no repositório.

## Verificação

O projeto não possui uma suíte de testes automatizados neste momento. A verificação principal é executar `python main.py` e conferir a criação de `saida/relatorio_divergencias.csv`.

## Publicação no GitHub

Depois de criar o repositório no GitHub, na pasta do projeto:

```powershell
git init
git add .
git commit -m "chore: prepara projeto de reconciliacao"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
git push -u origin main
```

Antes do `git add`, confira se o ambiente virtual e os artefatos locais não serão enviados:

```powershell
git status --short
```
