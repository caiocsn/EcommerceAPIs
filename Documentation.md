# E-commerce automation with microservices

## Design da solução

O projeto consiste de APIs REST independentes e escaláveis, que podem ser facilmente integradas por aplicações web ou mobile. Os dados de pedidos e inventário são armazenados em um banco de dados local, com a possibilidade de uso de uma solução mais robusta.

![Alt Text](images\archtecture1.jpg)

O sistema é controlado pelo script run.py, que configura as variáveis de ambiente, inicia os serviços (APIs) em servidores separados e exibe a interface gráfica. Essa interface permite realizar operações como criação de pedidos, itens e mudança de status, interagindo diretamente com as APIs. Todos os dados do E-commerce são armazenados no banco de dados, que é acessado através dos serviços.

## Funcionalidades

### Criação de pedidos
Os pedidos são criados via requisição à API de pedidos, onde são validadas as informações e verificada a disponibilidade dos itens no inventário. Caso atendam aos requisitos, os itens são deduzidos do estoque e calculada a fatura total. Pedidos que não atendem aos requisitos não são adicionados à base de dados.

**A verificação de disponibilidade de inventário é automática.**

### Pagamento
O fluxo de pagamento simula as funções de "confirmar" e "cancelar" para pedidos no estágio "criado", sem afetar pedidos em outros estágios. **A automação dessas operações requer integração com instituições financeiras que possibilitem a confirmação de pagamentos de forma automatizada.**

### Gerenciamento de Inventário

Este serviço é responsável por gerenciar o estoque, quantidades e registros de itens no inventário. Ele controla os níveis de mercadoria, atualiza quantidades, e valida novos pedidos. **A funcionalidade é principalmente automatizada, requerendo intervenção humana apenas para decidir quais pedidos serão registrados.**

### Envios
Essa funcionalidade gerencia os status de envio do pedido, com estágios válidos sendo "processando", "enviado" e "entregue". Apenas pedidos no estado "pago" podem ter seus status alterados por esse serviço. A atualização dos estados nem sempre é linear, podendo pular etapas logísticas. 

**A automação dessa etapa depende de integrações com sistemas de gerenciamento e provedores logísticos.**

## APIs

**Descrição da Aplicação**

A aplicação é composta por diversas APIs, cada uma responsável por uma funcionalidade específica do sistema. Para acessar cada API, é necessário utilizar os endereços definidos no arquivo init.py. Abaixo estão listados os endereços padrão de cada API:

- API de Pedidos: http://127.0.0.1:8010/
- API de Inventário: http://127.0.0.1:8011/
- API de Pagamentos: http://127.0.0.1:8012/
- API de Envios: http://127.0.0.1:8013/

**Documentação e Requisições Manuais**

Uma vez que a aplicação é executada, é possível realizar requisições manuais e depurações através da subrota `/docs` de cada API. Por exemplo, para acessar a API de Pedidos pelo navegador, você pode utilizar o seguinte endereço: http://127.0.0.1:8010/docs/

Ao acessar o endereço da documentação de cada API, será exibida uma interface interativa que permite visualizar os endpoints disponíveis, seus parâmetros, modelos de resposta e realizar testes diretamente no navegador.

**Observações**

- Certifique-se de que a aplicação esteja em execução antes de realizar qualquer requisição manual ou depuração.
- Através da documentação interativa, você poderá conhecer os detalhes e funcionalidades de cada API, facilitando o desenvolvimento, integração e depuração do sistema como um todo.

### Documentação da API - Sistema de Pedidos

A API é responsável por gerenciar pedidos e o estoque de itens associados. Abaixo estão detalhadas as funcionalidades principais, os endpoints disponíveis e as informações de uso.

**1. Endpoint: POST /orders/**

Este endpoint permite criar um novo pedido no sistema.

**Parâmetros:**

- **order:** Representa um objeto JSON contendo as informações do pedido a ser criado. O objeto deve seguir o modelo `OrderWrite` definido na documentação de modelos.

**Resposta:**

- **Código 200 OK:** O pedido foi criado com sucesso. A resposta contém as informações do pedido criado.

- **Código 404 Not Found:** Caso algum item do pedido não esteja disponível em estoque.

**2. Endpoint: GET /orders/**

Este endpoint permite ler informações sobre os pedidos existentes no sistema.

**Parâmetros:**

- **order_id (opcional):** Um número inteiro que representa o ID único do pedido a ser consultado. Se não for fornecido, serão retornados todos os pedidos cadastrados.

**Resposta:**

- **Código 200 OK:** A resposta contém uma lista de objetos JSON, onde cada objeto representa um pedido. Os pedidos são retornados no modelo `OrderRead`.

- **Código 404 Not Found:** Caso não haja nenhum pedido cadastrado ou se o pedido com o ID fornecido não for encontrado.

**Modelos:**

- **OrderWrite:** Representa o modelo para a criação de um pedido. Possui os seguintes campos:

  - **items (List[dict]):** Uma lista de dicionários contendo as informações dos itens do pedido. Cada dicionário deve conter os campos "product" (str) e "quantity" (int).
  
  - **customer_name (str):** O nome do cliente que está realizando o pedido.
  
  - **customer_email (str):** O e-mail do cliente que está realizando o pedido.

- **OrderRead:** Representa o modelo para leitura de um pedido existente. Possui os seguintes campos:

  - **id (int):** O ID único do pedido no sistema.
  
  - **items (List[dict]):** Uma lista de dicionários contendo as informações dos itens do pedido. Cada dicionário contém os campos "product" (str) e "quantity" (int).
  
  - **customer_name (str):** O nome do cliente que realizou o pedido.
  
  - **customer_email (str):** O e-mail do cliente que realizou o pedido.
  
  - **status (str):** O status atual do pedido (exemplo: "created", "processing", "completed").
  
  - **total (float):** O valor total do pedido.

### Documentação da API - Gerenciamento de Itens

A API oferece funcionalidades para criar, ler, atualizar e deletar itens no sistema, além de permitir a subtração de quantidades de itens do estoque.

**1. Endpoint: POST /items/**

Este endpoint permite criar um novo item no sistema.

**Parâmetros:**

- **item:** Representa um objeto JSON contendo as informações do item a ser criado. O objeto deve seguir o modelo `Item` definido na documentação de modelos.

**Resposta:**

- **Código 200 OK:** O item foi criado com sucesso. A resposta contém as informações do item criado.

- **Código 400 Bad Request:** Caso o ID fornecido não seja único.

**2. Endpoint: GET /items/**

Este endpoint permite ler informações sobre os itens existentes no sistema.

**Parâmetros:**

- **item_ids (opcional):** Uma lista de números inteiros que representa os IDs dos itens a serem consultados. Se não for fornecida, serão retornados todos os itens cadastrados.

**Resposta:**

- **Código 200 OK:** A resposta contém uma lista de objetos JSON, onde cada objeto representa um item. Os itens são retornados no modelo `Item`.

- **Código 404 Not Found:** Caso não haja nenhum item cadastrado ou se os itens com os IDs fornecidos não forem encontrados.

**3. Endpoint: PUT /items/{item_id}**

Este endpoint permite atualizar as informações de um item existente no sistema.

**Parâmetros:**

- **item_id:** Um número inteiro que representa o ID único do item a ser atualizado.

- **item:** Representa um objeto JSON contendo as informações atualizadas do item. O objeto deve seguir o modelo `Item` definido na documentação de modelos.

**Resposta:**

- **Código 200 OK:** O item foi atualizado com sucesso. A resposta contém as informações atualizadas do item.

- **Código 400 Bad Request:** Caso o ID fornecido não seja único.

- **Código 404 Not Found:** Caso o item com o ID fornecido não seja encontrado.

**4. Endpoint: DELETE /items/{item_id}**

Este endpoint permite deletar um item existente no sistema.

**Parâmetros:**

- **item_id:** Um número inteiro que representa o ID único do item a ser deletado.

**Resposta:**

- **Código 200 OK:** O item foi deletado com sucesso. A resposta contém as informações do item que foi deletado.

- **Código 404 Not Found:** Caso o item com o ID fornecido não seja encontrado.

**5. Endpoint: PUT /items/subtract/**

Este endpoint permite subtrair quantidades de itens do estoque.

**Parâmetros:**

- **items_to_subtract:** Um dicionário JSON onde as chaves representam os IDs dos itens a serem subtraídos e os valores representam as quantidades a serem subtraídas.

**Resposta:**

- **Código 200 OK:** Os itens foram subtraídos do estoque com sucesso. A resposta contém uma mensagem de sucesso e o total da operação.

- **Código 400 Bad Request:** Caso a quantidade a ser subtraída seja inválida ou se algum item não for encontrado.

- **Código 404 Not Found:** Caso algum item com os IDs fornecidos não seja encontrado.

**Modelo:**

- **Item:** Representa o modelo para criação, leitura e atualização de um item. Possui os seguintes campos:

  - **id (int):** O ID único do item no sistema.
  
  - **name (str):** O nome do item.
  
  - **description (str):** A descrição do item.
  
  - **price (float):** O preço do item.
  
  - **quantity (int):** A quantidade disponível em estoque do item.

### Documentação da API - Gerenciamento de Pagamentos

A API oferece funcionalidades para confirmar ou cancelar pagamentos de pedidos no sistema.

**1. Endpoint: POST /payments/confirm/{order_id}**

Este endpoint permite confirmar o pagamento de um pedido existente no sistema.

**Parâmetros:**

- **order_id:** Um número inteiro que representa o ID único do pedido a ser confirmado.

**Resposta:**

- **Código 200 OK:** O pagamento foi confirmado com sucesso. A resposta contém as informações atualizadas do pedido confirmado, no modelo `OrderRead`.

- **Código 400 Bad Request:** Caso o status atual do pedido não seja "created", ou seja, se ele não estiver em estado de pagamento pendente.

- **Código 404 Not Found:** Caso o pedido com o ID fornecido não seja encontrado.

**2. Endpoint: POST /payments/cancel/{order_id}**

Este endpoint permite cancelar o pagamento de um pedido existente no sistema.

**Parâmetros:**

- **order_id:** Um número inteiro que representa o ID único do pedido a ser cancelado.

**Resposta:**

- **Código 200 OK:** O pagamento foi cancelado com sucesso. A resposta contém as informações atualizadas do pedido cancelado, no modelo `OrderRead`.

- **Código 400 Bad Request:** Caso o status atual do pedido não seja "created", ou seja, se ele não estiver em estado de pagamento pendente.

- **Código 404 Not Found:** Caso o pedido com o ID fornecido não seja encontrado.

**Modelo:**

- **OrderRead:** Representa o modelo para leitura de um pedido existente. Possui os seguintes campos:

  - **id (int):** O ID único do pedido no sistema.
  
  - **items (List[dict]):** Uma lista de dicionários contendo as informações dos itens do pedido. Cada dicionário contém os campos "product" (str) e "quantity" (int).
  
  - **customer_name (str):** O nome do cliente que realizou o pedido.
  
  - **customer_email (str):** O e-mail do cliente que realizou o pedido.
  
  - **status (str):** O status atual do pedido (exemplo: "created", "processing", "delivered").
  
  - **total (float):** O valor total do pedido.

### Documentação da API - Gerenciamento de Envio de Pedidos

A API oferece funcionalidades para atualizar o status de envio de pedidos no sistema, indicando as etapas de processamento, envio e entrega.

**1. Endpoint: POST /shipping/processing/{order_id}**

Este endpoint permite atualizar o status de um pedido para "processing", indicando que o pedido está em processo de preparação para o envio.

**Parâmetros:**

- **order_id:** Um número inteiro que representa o ID único do pedido a ser atualizado.

**Resposta:**

- **Código 200 OK:** O status do pedido foi atualizado com sucesso para "processing". A resposta contém as informações atualizadas do pedido, no modelo `OrderRead`.

- **Código 400 Bad Request:** Caso o status atual do pedido não seja "payed", ou seja, se o pagamento ainda não foi confirmado.

- **Código 404 Not Found:** Caso o pedido com o ID fornecido não seja encontrado.

**2. Endpoint: POST /shipping/sent/{order_id}**

Este endpoint permite atualizar o status de um pedido para "sent", indicando que o pedido foi enviado ao destinatário.

**Parâmetros:**

- **order_id:** Um número inteiro que representa o ID único do pedido a ser atualizado.

**Resposta:**

- **Código 200 OK:** O status do pedido foi atualizado com sucesso para "sent". A resposta contém as informações atualizadas do pedido, no modelo `OrderRead`.

- **Código 400 Bad Request:** Caso o status atual do pedido não seja "processing" ou "payed", ou seja, se o pedido ainda não está em processo de preparação ou se o pagamento ainda não foi confirmado.

- **Código 404 Not Found:** Caso o pedido com o ID fornecido não seja encontrado.

**3. Endpoint: POST /shipping/delivered/{order_id}**

Este endpoint permite atualizar o status de um pedido para "delivered", indicando que o pedido foi entregue ao destinatário.

**Parâmetros:**

- **order_id:** Um número inteiro que representa o ID único do pedido a ser atualizado.

**Resposta:**

- **Código 200 OK:** O status do pedido foi atualizado com sucesso para "delivered". A resposta contém as informações atualizadas do pedido, no modelo `OrderRead`.

- **Código 400 Bad Request:** Caso o status atual do pedido não seja "processing", "payed" ou "sent", ou seja, se o pedido ainda não está em processo de preparação, se o pagamento ainda não foi confirmado ou se o pedido ainda não foi enviado.

- **Código 404 Not Found:** Caso o pedido com o ID fornecido não seja encontrado.

**Modelo:**

- **OrderRead:** Representa o modelo para leitura de um pedido existente. Possui os seguintes campos:

  - **id (int):** O ID único do pedido no sistema.
  
  - **items (List[dict]):** Uma lista de dicionários contendo as informações dos itens do pedido. Cada dicionário contém os campos "product" (str) e "quantity" (int).
  
  - **customer_name (str):** O nome do cliente que realizou o pedido.
  
  - **customer_email (str):** O e-mail do cliente que realizou o pedido.
  
  - **status (str):** O status atual do pedido (exemplo: "created", "processing", "payed", "sent", "delivered").
  
  - **total (float):** O valor total do pedido.
