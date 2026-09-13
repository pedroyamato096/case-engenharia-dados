# Reconciliação de pedidos

Solução do case técnico de Engenharia de Dados. O projeto reconstrói o estado atual dos pedidos a partir do log de eventos, compara o resultado com a tabela analítica e gera um relatório de divergências.

## Tecnologias

- Python 3.12 ou superior
- pandas para leitura, normalização e comparação dos CSVs
- pytest para testes automatizados
- Git e GitHub para versionamento e entrega

Não há necessidade de banco de dados, Docker ou ferramenta de orquestração para o volume e o escopo deste case. A solução pode ser executada localmente do início ao fim.

## Preparação no Windows

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

## Estrutura

```text
.
|-- dados\       # CSVs recebidos para o case
|-- saida\       # relatórios gerados
|-- main.py      # ponto de entrada
|-- requirements.txt
|-- RESUMO.md
|-- DECISOES.md
`-- CASE_Engenharia_de_Dados.md
```

Coloque `pedidos_origem.csv` e `pedidos_destino.csv` em `dados\`. O comando de execução e os nomes exatos dos arquivos serão definidos no código final.

## Execução

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

## Testes

```powershell
python -m pytest
```

## Publicação no GitHub

Crie um repositório vazio no GitHub, sem README, `.gitignore` ou licença. Depois, na pasta do projeto:

```powershell
git init
git add .
git commit -m "chore: prepara projeto de reconciliacao"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
git push -u origin main
```

Antes do `git add`, confira se os arquivos de entrada e o ambiente virtual não serão enviados:

```powershell
git status --short
```
