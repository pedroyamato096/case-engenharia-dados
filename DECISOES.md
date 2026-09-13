# Decisões técnicas

> Atualizar este documento durante a análise dos dados. A justificativa das decisões é parte da entrega.

## Decisões tomadas

A análise dos arquivos foi realizada antes da reconstrução do estado atual dos pedidos. Nesta etapa, não foram aplicadas regras de comparação ou classificação de divergências.

A origem será tratada como um histórico de eventos, e não como uma lista de pedidos, pois contém 474 linhas para 150 pedidos únicos. O destino contém 137 linhas para 133 pedidos únicos, incluindo quatro IDs duplicados.

As regras para escolher o estado final, tratar exclusões, normalizar status e lidar com valores ausentes serão definidas após a análise detalhada dos históricos.

## Casos sem resposta única

A análise inicial identificou situações que exigirão critérios explícitos:

- A origem contém três eventos com `valor_total` vazio: pedidos `10064`, `10098` e `10119`.
- O destino possui quatro IDs duplicados: `10002`, `10032`, `10079` e `10127`.
- Os status não estão representados de maneira uniforme no destino. Há diferenças de maiúsculas, minúsculas e espaços, como `enviado`, `ENVIADO `, `entregue` e `PAGO `.
- As datas possuem formatos diferentes: a origem usa data, hora e fuso horário; o destino não informa o fuso horário.
- A origem possui operações `I`, `U` e `D`, mas ainda será necessário definir como interpretar o estado final quando houver exclusão ou eventos fora de ordem.

Esses casos não foram classificados como divergências nesta etapa, pois primeiro é necessário definir as regras de interpretação.

## Premissas assumidas

- A origem é um histórico de eventos, portanto vários registros com o mesmo `id_pedido` são esperados.
- O `id_pedido` é a chave usada para relacionar origem e destino.
- Os valores de `status` deverão ser normalizados para permitir comparação sem considerar diferenças de caixa ou espaços externos.
- As diferenças de formato das datas não serão consideradas divergências automaticamente.
- Um campo vazio na origem não será substituído por um valor inventado. O tratamento será definido durante a reconstrução do estado atual.

## Limitações

- A captura da origem pode ter começado depois que alguns pedidos já existiam.
- O log pode conter eventos duplicados ou eventos ausentes.
- Não existe, aparentemente, um identificador único do evento que permita distinguir duplicidade real de duas ocorrências idênticas.
- O destino contém IDs repetidos, portanto não pode ser tratado automaticamente como uma tabela com uma linha garantida por pedido sem investigação adicional.
- As datas do destino não possuem informação de fuso horário, o que pode limitar uma comparação temporal exata.
- Os resultados dependem das regras adotadas para os casos ambíguos.

## Uso de IA

Utilizei GitHub Copilot para apoiar a preparação do ambiente, a organização inicial do projeto e a revisão do código. As decisões de negócio, os critérios de reconciliação e a validação dos resultados devem ser revisados e explicados por mim.
