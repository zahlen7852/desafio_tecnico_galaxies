# **🏢 Case Técnico – Andrômeda (Empresa Fictícia)**

## **📖 Contexto Geral**

A **Andrômeda** é uma empresa de e-commerce em rápida expansão.

Atualmente, o time de Dados está enfrentando problemas relacionados a:

- **Qualidade e consistência dos dados transacionais**
- **Integração de dados externos**
- **Definição de uma arquitetura moderna e escalável**

Você foi convidado(a) para participar de um desafio técnico que avalia suas habilidades em **SQL**, **Python** e **Arquitetura de Dados**.

# **Problema 1**

A empresa possui uma base de **transações e produtos** em um banco relacional (Postgres ou MySQL). O time necessita ter uma visão de quantos itens foram vendidos no dia por importância de categorias, bem como a quantidade de itens e seu ticket médio.

Base de **transações**:

transactions.csv - *vide anexo e-mail*

Base de **produtos:**

products.csv - *vide anexo e-mail*

**Query** existente:

query.sql - *vide anexo e-mail*

### **Problemas relatados:**

1. **category_importance** vem nula para alguns casos.
2. **total_value** não bate com o esperado.
3. O **agrupamento está duplicando usuários em um mesmo dia**.
4. Por algum motivo, a query parou de funcionar depois do dia 3 de agosto de 2025.

### **Sua tarefa:**

- Analisar a query existente e identificar **possíveis problemas** nos cálculos, agrupamentos e regras de categorização.
- Propor e implementar as **correções necessárias**.
- Entregar:
    1. A **query final corrigida**;
    2. Um breve **relato dos principais problemas encontrados** e como foram ajustados.

### **Dica:**

- O problema não necessariamente é a query. Encontre formas de contornar a situação.

# **Problema 2 - Extração de dados de fontes externas**

A **Andrômeda** quer integrar dados externos para uma campanha do **Pokémon do Dia das Crianças**.

Os analistas necessitam de **todos os dados de todos os Pokémon**, incluindo habilidades e moveset. Qualquer dado adicional que enriqueça possíveis análises é bem-vindo.

Foi disponibilizada uma **API pública**: [Poke API](https://pokeapi.co/docs/v2#pokemon).

### **Sua tarefa:**

- Extrair **todos os Pokémon disponíveis na API**, incluindo pelo menos:
    - **id, name, base_experience, height, weight, generation**
    - lista de **abilities**,
    - lista de **moves**.
- Modelar os dados extraídos para armazenamento em um **banco relacional** (pode ser Postgres ou MySQL).
- Você está livre para definir o modelo de dados:
    - Pode optar por **um modelo relacional normalizado**,
    - Ou por um modelo **star schema** (fato e dimensões),
    - Ou até mesmo um formato mais **denormalizado,** dependendo da sua estratégia.

### **Entrega esperada:**

1. Script Python que:
    - Consome a API com paginação (ou simulação de paginação em blocos).
    - Faz o parsing dos dados de cada Pokémon.
    - Salva os dados no banco de dados local.
2. Modelo de dados proposto:
    - Criação da(s) tabela(s) (DDL).
    - Descrição breve das escolhas feitas (por que normalizou ou denormalizou, por exemplo).

### **Dicas:**

- Use ferramentas como **Postman** para explorar a API e entender melhor os endpoints.
- Lembre-se de que a API pode retornar listas longas (por exemplo, moves e abilities), então pense em como modelar isso no banco.
- O código não precisa ser altamente otimizado, mas precisa ser **claro, organizado e funcional**.

# **Problema 3 – Arquitetura de Dados**

Hoje os dados da **Andrômeda** estão dispersos:

- Transações em um banco NoSQL (MongoDB).
- Produtos em arquivos CSV.
- Logs de navegação em JSON.
- Integrações externas em APIs.

A diretoria quer centralizar isso em uma arquitetura moderna.

### **Três opções discutidas foram:**

1. **Data Lake puro no Cloud Storage** + analistas lendo via queries ad hoc.
2. **ETL manual** (scripts Python agendados) carregando direto em tabelas analytics.
3. **Pipeline estruturado**:
    - Camada raw no **Cloud Storage**;
    - Transformações no **BigQuery** (staging → analytics);
    - Orquestração com **Cloud Composer (Airflow)**;
    - Consumo via **Looker Studio (ou qualquer ferramenta dataviz)**.

### **Sua tarefa:**

- Escolher qual modelo seria o mais adequado para a **Andrômeda**.
- Justificar sua escolha com base em:
    - Governança
    - Escalabilidade
    - Manutenção
    - Custos
- **Entregar um desenho técnico** da arquitetura proposta (pode ser feito em [draw.io](http://draw.io/), Lucidchart, Miro ou até mesmo em papel e enviado como imagem).

### Anexos

**Bases:**

[products.csv](attachment:2d9e6685-9cec-4d0e-9f17-7e796305a38c:products.csv)

[transactions.csv](attachment:34b044a5-26c4-42ea-8d3e-5ebacbe76d1b:transactions.csv)

Query:

[query.sql](attachment:a9fe0fec-281b-49f5-966f-5020988d0fca:query.sql)