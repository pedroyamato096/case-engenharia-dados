## Decisões tomadas

### Reconstrução do estado atual

A origem foi tratada como um histórico de eventos, e não como uma lista de pedidos. Ela contém 474 linhas para 150 pedidos únicos, enquanto o destino contém 137 linhas para 133 pedidos únicos.

Para reconstruir a origem, os eventos são ordenados por `id_pedido`, `atualizado_em` e pela ordem original da linha. Depois, é selecionado o último evento de cada pedido. A operação `D` é interpretada como exclusão: pedidos cujo último evento é `D` são separados e não entram na origem ativa comparada com o destino.

Escolhi o evento mais recente pela data porque o arquivo informa quando o evento ocorreu, embora os eventos tenham chegado fora de ordem. Não usei a posição original como critério principal, pois ela representa a chegada pela fila, não necessariamente a ocorrência no sistema.

### Normalização antes da comparação

Status são comparados após remover espaços externos e converter para maiúsculas. Valores monetários são convertidos para número. Datas são convertidas para UTC.

Essa escolha evita falsos positivos causados apenas por representação, como `pago`, `PAGO ` e `PAGO`. Não normalizei valores ausentes para um valor inventado, porque isso poderia fabricar informação que não existe no histórico.

O destino não informa fuso horário. Nos dados observados, seus horários correspondem aos horários da origem convertidos para UTC, com diferença fixa de três horas. Por isso, os horários sem fuso do destino foram interpretados como UTC. Essa é uma decisão baseada nos dados, não uma garantia fornecida pelo arquivo.

### Classificação das divergências

As divergências foram separadas em problemas de existência, estrutura e conteúdo:

- `AUSENTE_NO_DESTINO`: o pedido existe na origem ativa, mas não no destino;
- `INDEVIDO_NO_DESTINO`: o destino possui um pedido que não existe na origem ativa;
- `DUPLICADO_NO_DESTINO`: o pedido existe nos dois lados, mas aparece mais de uma vez no destino;
- divergência de um campo, como `STATUS_DIVERGENTE` ou `VALOR_TOTAL_DIVERGENTE`;
- `MULTIPLOS_CAMPOS_DIVERGENTES`: mais de um atributo está diferente.

Pedidos duplicados não são comparados campo a campo. Como há mais de uma linha possível no destino, não seria correto escolher uma delas arbitrariamente. Primeiro o problema estrutural precisa ser resolvido.

O impacto financeiro foi calculado como o total dos valores da origem ativa menos o total dos valores do destino. Esse número mostra a diferença entre os relatórios, mas não prova que toda a diferença seja causada exclusivamente pelos pedidos classificados como divergentes.

## Casos sem resposta única

Estes casos exigem uma decisão justificável, pois os arquivos não fornecem informação suficiente para uma resposta única:

- **Eventos com o mesmo timestamp:** não existe um identificador sequencial do evento. Quando dois eventos do mesmo pedido têm a mesma data e hora, considerei mais recente o que aparece depois no arquivo. Essa escolha torna o resultado determinístico, mas não garante a ordem real dos acontecimentos.
- **Datas do destino sem fuso:** interpretei-as como UTC porque essa regra elimina a diferença fixa de três horas observada em relação à origem. Outra interpretação, como `America/Sao_Paulo`, criaria divergências artificiais.
- **Valores vazios:** a origem possui valor vazio nos pedidos `10064`, `10098` e `10119`. Mantive o valor como ausente e não o substituí por zero ou pelo valor de outro evento, pois não há base suficiente para fazer essa imputação.
- **Eventos `D`:** considerei que um pedido cujo último evento é uma exclusão não deve aparecer no destino. Não tratei um evento anterior como estado ativo, pois isso ignoraria a última operação registrada.
- **Duplicidades no destino:** há IDs duplicados, incluindo `10002`, `10032`, `10079` e `10127`. Reportei a duplicidade sem escolher qual linha é a correta, porque o arquivo não fornece um critério confiável para desempate.
- **Diferenças de status, caixa e espaços:** considerei equivalentes as diferenças de formatação, como `enviado` e `ENVIADO `. Sem essa regra, o relatório teria falsos positivos.

## Premissas assumidas

- `id_pedido` é a chave de negócio correta para relacionar origem e destino.
- Depois da reconstrução, deve existir no máximo uma linha ativa por pedido na origem.
- O maior valor de `atualizado_em` representa o evento mais recente do pedido.
- A ordem original do arquivo só pode ser usada como desempate técnico, não como prova de cronologia.
- A operação `I` representa criação, `U` alteração e `D` exclusão, conforme o enunciado.
- Diferenças de espaços, maiúsculas e formatos de data não representam necessariamente diferenças de negócio.
- Um valor ausente em apenas um dos lados é uma divergência; dois valores ausentes são tratados como equivalentes.
- O destino deveria ter uma única linha por pedido ativo.
- Os pedidos ausentes na origem não podem ser considerados válidos no destino, mesmo que a captura da origem possa ter começado depois de o sistema já existir.
- O campo `id_cliente` faz parte do estado comparável do pedido, mas não é usado para agrupar eventos. O agrupamento é feito somente por `id_pedido`.

## Limitações

- **Captura incompleta:** a origem pode ter começado depois que pedidos já existiam. Nesse caso, um pedido pode estar no destino sem aparecer no histórico disponível, e a solução o classificará como `INDEVIDO_NO_DESTINO`, embora a causa real seja falta de histórico.
- **Eventos ausentes ou duplicados:** a fila não garante entrega única nem completa. Se o evento mais recente não estiver no arquivo, a reconstrução poderá escolher um estado antigo. Sem um identificador único do evento, também não é possível distinguir uma repetição exata de dois eventos legítimos iguais.
- **Empate de timestamps:** eventos com a mesma data e hora continuam ambíguos. A ordem do arquivo apenas torna o processamento reproduzível; se a ordem das linhas mudar, o resultado desses pedidos pode mudar.
- **Fuso horário do destino:** a interpretação como UTC foi inferida dos dados. Se o sistema de destino usar outro fuso ou misturar convenções, a comparação de datas poderá gerar falsos positivos ou falsos negativos.
- **Duplicidade no destino:** a solução identifica e reporta IDs duplicados, mas não corrige a tabela nem escolhe automaticamente o registro correto. Essa correção precisa de uma regra de negócio adicional.
- **Valores ausentes:** a solução não imputa valores vazios. Isso evita inventar dados, mas deixa alguns pedidos dependentes de uma decisão posterior do negócio.
- **Escala e memória:** o código atual lê os CSVs completos em `pandas` e mantém os DataFrames em memória. Para um volume mil vezes maior, isso pode consumir muita memória e tornar o processamento lento ou inviável.
- **Arquivo CSV:** a solução depende de arquivos CSV com estrutura e formatos compatíveis. Não há controle de esquema, catálogo de dados, conexão incremental ou monitoramento de uma carga recorrente.
- **Validação automatizada:** a execução e a sintaxe foram verificadas, mas o projeto ainda não possui uma suíte completa de testes automatizados cobrindo todos os casos ambíguos e cenários de erro.
- **Impacto financeiro:** o valor apresentado é uma diferença agregada entre os totais dos dois conjuntos. Ele não atribui causalidade individual a cada pedido e não substitui uma análise financeira dos pedidos divergentes.

## Uso de IA

Utilizei o Codex durante o desenvolvimento, de forma declarada e como apoio, não como substituto da análise. As atividades apoiadas foram:

- preparação e organização inicial do projeto Python;
- leitura e inspeção dos CSVs para entender quantidade de linhas, IDs e formatos;
- explicação de conceitos de pandas usados no trabalho, como `sort_values`, `kind="stable"`, `groupby`, `as_index`, `reset_index`, `.loc`, conjuntos e índices;
- discussão das regras para selecionar o último evento, tratar exclusões, duplicidades, valores ausentes e fusos horários;
- revisão e simplificação do código para deixá-lo mais compreensível;
- integração do `main.py` com os módulos existentes em `src`;
- execução de validações, verificação de sintaxe e conferência dos resultados;


