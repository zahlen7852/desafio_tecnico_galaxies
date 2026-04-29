# Problema número 1

No products.csv  - foi encontrado um campo com erro de digitação para a categoria 'Clothing', o registro está como 'Clothng'.

```
product_id,product_name,category
1,Laptop,Electronics 
2,Headphones,Electronics
3,Office Chair,Furniture
4,Notebook,Stationery
5,Book,Books
6,T-Shirt,Clothng
7,Action Figure,Toys
8,Gift Card,Electronics
```

Na query dentro do CASE, as categorias estão definidas erroneamente, 'Electronics' foi escrito como 'Electonics' e a categoria 'Toys' como 'toys'

```sql
            CASE
                WHEN p.category = 'Electonics' THEN 'High'
                WHEN p.category = 'Books' THEN 'Medium'
                WHEN p.category = 'Furniture' THEN 'Low'
                WHEN p.category = 'Stationery' THEN 'Low'
                WHEN p.category = 'Clothing' THEN 'Low'
                WHEN p.category = 'toys' THEN 'Low'
                ELSE NULL
            END AS category_importance,
```

Correções necessárias na query:

Para que não ocorra a diferenciação entre letras maiusculas e minúsculas, precisamos padronizar, podemos utilizar LOWER para deixarmos tudo minúsculo, por exemplo.

Os erros de Typo estavam influenciando no agrupamento causando uma divergência no total_value, é possível tanto tratar os dados passando clothng para clothing para quanto incluir esses valores 'errados' no CASE responsável por criar a coluna category_importance:

```sql
   CASE
       WHEN p.category_norm = 'electronics' THEN 'High'
       WHEN p.category_norm = 'books' THEN 'Medium'
       WHEN p.category_norm IN ('furniture', 'stationery', 'clothng', 'clothing', 'toys') THEN 'Low'
       ELSE 'Unknown'
   END AS category_importance,
```





casos pontuais podem ser feitos dessa forma, considerando uma volumetria maior e em caso de uso real, entendo que esses dados precisam estar harmonizados antes de serem disponibilizados para uma query analítica.

A query inicial agrupava por transaction_id, ou seja, permitia uma visualização separada por transação e não uma visão do dia ou por usuário.

Para olhar o dia e ter uma visão do consumo por usuário distintos, é necessário remover transaction_id do GROUP BY e incluir COUNT(DISTINCT user_id) como coluna.

No caso da query não funcionar a partir do dia 03/08/2025 está relacionado a um registro com quantitiy = 0 ao fazer a divisão por 0, imagino que esteja dando erro, a correção seria a inclusão de NULLIF(SUM(quantity), 0) e possívelmente um filtro de qualidade quantity > 0 nos dados de transactions isso em uma etapa posterior ou se a query for feita utilizando CTEs (fica mais fácil de organizá-la).

```sql
WITH products_clean AS (
   SELECT
       product_id,
       product_name,
       LOWER(TRIM(category)) AS category_norm
   FROM products
),
transactions_clean AS (
   SELECT
       transaction_id,
       user_id,
       product_id,
       quantity,
       price,
       DATE(transaction_date) AS transaction_day
   FROM transactions
   WHERE quantity > 0
)
SELECT
   t.transaction_day,
   CASE
       WHEN p.category_norm = 'electronics' THEN 'High'
       WHEN p.category_norm = 'books' THEN 'Medium'
       WHEN p.category_norm IN ('furniture', 'stationery', 'clothng', 'clothing', 'toys') THEN 'Low'
       ELSE 'Unknown'
   END AS category_importance,
   SUM(t.quantity) AS total_quantity,
   SUM(t.price * t.quantity) AS total_value,
   SUM(t.price * t.quantity) / NULLIF(SUM(t.quantity), 0) AS avg_ticket,
   COUNT(DISTINCT t.user_id) AS distinct_users
FROM transactions_clean t
LEFT JOIN products_clean p
   ON t.product_id = p.product_id
GROUP BY
   t.transaction_day,
   CASE
       WHEN p.category_norm = 'electronics' THEN 'High'
       WHEN p.category_norm = 'books' THEN 'Medium'
       WHEN p.category_norm IN ('furniture', 'stationery', 'clothng', 'clothing', 'toys') THEN 'Low'
       ELSE 'Unknown'
   END
ORDER BY
   t.transaction_day,
   category_importance;
```
