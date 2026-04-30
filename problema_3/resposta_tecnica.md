# Problema 3

## Escolha da arquitetura

A melhor opcao para a Andromeda e a **Opcao 3 (Pipeline estruturado)**:

- Camada raw no Cloud Storage
- Transformacoes no BigQuery (staging -> analytics)
- Orquestracao com Cloud Composer (Airflow)
- Consumo em Looker Studio

Essa abordagem atende melhor aos criterios de governanca, escalabilidade, manutencao e custo para um cenario com multiplas fontes (MongoDB, CSV, JSON e APIs).

## Justificativa tecnica

### 1) Governanca

- A separacao em camadas (`raw`, `staging`, `analytics`) cria rastreabilidade clara do dado.
- A camada `raw` preserva o dado original, importante para auditoria e reprocessamento.
- No BigQuery, é possivel aplicar controle de acesso por dataset/tabela e masking quando necessário.
- A orquestração no Airflow ajuda a padronizar execuções, logs, alertas, tags e SLA.

### 2) Escalabilidade

- GCS escala para grandes volumes de arquivos semi-estruturados e estruturados com baixo custo.
- BigQuery escala horizontalmente e é serverless, ou seja, abstrai o gerenciamento de infraestrutura.
- A arquitetura suporta inclusao de novas fontes e pipelines sem ser necessário configurar outro serviço ou ajustar algum componente da plataforma de dados.

### 3) Manutencao

- DAGs no Airflow centralizam agendamentos e dependencias entre etapas e observabilidade para as pipelines..
- Reprocessamento por partição (ex.: data) reduz risco e custo operacional.
- Separar ingestao e transformacao simplifica testes e evolução de regras de negocio.
- Disponibilizar os dados na camada `analytics` reduz a quantidade de transformações necessárias no BI pois os dados já estão 'prontos'.

### 4) Custos

- Armazenamento é mais barato do que processamento, falando de big data, utilizar uma modelagem em camadas reduz drásticamente a quantidade de reprocessamento dos dados como um todo em caso de erros já que são escritos ao longo das camadas aumentado granularidade, ou seja, temos vários "checkpoints".
- A cobrança do BigQuery funciona como 'pay as you go', então se usado corretamente (resultado da relação entre volumetria e latencia) tende a ser mais barato do quê manter um cluster ou infraestrutura on-premises rodando 24hrs.
- A utilização do Airflow para a orquestração de DAGs além de diminuir a quantidade de tempo necessário para executar e acompanhar as dags, o tempo de resposta aumenta, já que nem sempre será possível acompanhar a DAG durante todo o seu andamento, quando uma pipeline quebra e isso demora a ser resolvido, a depender da criticidade pode resultar em impacto financeiro e operacional para outros setores.

Em resumo, a opção 3 permite a escalabilidade operacional não apenas considerando volumetria de dados, mas também múltiplas pipelines e políticas de governança, e utilizando o Airflow específicamente, a parte de monitoramento e alerta das DAGs se torna extremamente simplificada.
