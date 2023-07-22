# Automação E-commerce

A aplicação implementa APIs REST e uma interce gráfica que automatizam o processamento de pedidos provinientes de vendas online.

## Sobre
O projeto é composto por APIs REST que funcionam como serviços independentes, proporcionando facilidade de manutenção e escalabilidade. Essas APIs podem ser facilmente integradas por aplicações convencionais, web ou mobile, permitindo a incorporação de diversas soluções distintas.

As informações de pedidos e inventário são armazenadas em um banco de dados local, mas com a flexibilidade de substituição por uma solução online e comercial, viabilizando a criação de dashboards em tempo real com base nos dados do processo.

Para o desenvolvimento, foi utilizado o framework FASTAPI, conhecido por sua eficiência e velocidade em aplicações web RESTful. Além disso, a interface gráfica foi implementada com tkinter, ideal para aplicativos desktop Python.

Apesar de terem sido reduzidos os comentários no código, o foco foi em estruturas interpretáveis e na produção de um código limpo, minimizando o ruído visual.

Para obter informações detalhadas sobre o projeto e seu funcionamento, é recomendado consultar a documentação  (Documentation.md).

## Instalação

Para utilizar o software é necessário ter o Python 3 instalado e configurado em sua máquina.

### Clone o respositório
No seu terminal execute os comando a seguir para clonar o projeto e acessar seu diretório:

```shell
$ git clone https://github.com/caiocsn/EcommerceAPIs
```
```shell
$ cd EcommerceAPIs
```

### Crie um ambiente virtual (opcional)
Antes de instalar as dependências do projeto é recomendado criar um novo ambiente virtual em sua máquina, evitando assim que a instalação dos novos pacotes cause problemas de combatibilidade a outros projetos.

Crie um novo ambiente (os arquivos do ambiente serão salvos no diretório em que o comando foi executado)
```shell
$ python -m venv myenv
```

Ative o ambiente virtual:
- Windows:
```shell
$ myenv\Scripts\activate
```
- Linux:
```shell
$ source venv_name/bin/activate
```

### Instale as dependências do projeto
As dependências do projeto estão especificadas no arquivo **requirement.txt** e podem ser instaladas atráves do comando: 

```shell
$ pip install -r requirements.txt
```

### Crie o banco de dados e aplique as migrações
A solução utiliza um banco de dados local SQLITE que deve ser criado a partir do comando:

```shell
$ alembic upgrade head 
```
### Rode o projeto
Com o ambiente configurado o projeto pode ser executado através do comando:
```shell
$ python run.py
```


## Implementações futuras
- Implementar timestamp dos eventos de criação e transição de estado
- Habilitar carregamento de pedidos e itens em lote, a partir de arquivo.
