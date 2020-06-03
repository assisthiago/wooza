# wooza
_API de gerenciamento de planos telefônicos onde é possível criar, consultar, editar e deletar os planos._

## Navegação
- Instalação
  - [Clonando o projeto](https://github.com/assisthiago/wooza/new/master?readme=1#clonando-o-projeto)
  - [Instalação dos requisitos](https://github.com/assisthiago/wooza/new/master?readme=1#instala%C3%A7%C3%A3o-dos-requisitos)
  - [Configuração o postgresql](https://github.com/assisthiago/wooza/new/master?readme=1#configura%C3%A7%C3%A3o-o-postgresql)
  - [Configuração o projeto](https://github.com/assisthiago/wooza/new/master?readme=1#configura%C3%A7%C3%A3o-o-projeto)
- API
  - [API de Criação](https://github.com/assisthiago/wooza/new/master?readme=1#api---cria%C3%A7%C3%A3o)
  - [API de Edição](https://github.com/assisthiago/wooza/new/master?readme=1#api---edi%C3%A7%C3%A3o)
  - [API de Deleção](https://github.com/assisthiago/wooza/new/master?readme=1#api---dele%C3%A7%C3%A3o)
  - [API de Consulta](https://github.com/assisthiago/wooza/new/master?readme=1#api---consulta)
    - [Busca](https://github.com/assisthiago/wooza/new/master?readme=1#busca)

## Instalação
- Tutorial disponível para o sistema MacOS.

### Clonando o projeto
Clonar o projeto e entrar na pasta raiz do projeto.
```
$ git clone git@github.com:<git_user>/wooza.git
...
$ cd wooza/
```

### Instalação dos requisitos

Instalar o Homebrew.
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Instalar o Python3.
```
$ brew install python3
```

Instalar o Virtualenv.
```
$ pip install virtualenv
```

Ainda na pasta raiz do projeto, criar um ambiente virtual.
```
$ virtualenv venv -p python3
```

Ativar o ambiente virtual.
```
$ source venv/bin/active
```
_Para desativar basta rodar o comando_: `$ deactive`

Ainda no ambiente virtual, instalar as dependências.
```
(venv) $ pip install -r requirements.txt
```
_Para verificar se tudo fora instalado corratamente basta rodar o comando_: `$ pip freeze`

### Configuração o postgresql

Instalar o Postgresql.
```
(venv) $ brew install postgresql
```

Criar o banco de dados.
```
(venv) $ createdb wooza_db
```

Entrar no banco de dados.
```
(venv) $ psql wooza_db
```

Criar o super usuário para o banco de dados.
```
> CREATE USER username WITH PASSWORD 'password';
> ALTER ROLE username SET client_encoding TO 'utf8';
> ALTER ROLE username SET default_transaction_isolation TO 'read committed';
> ALTER ROLE username SET timezone TO 'UTC';
```

Dar as permissões criadas acima do banco de dados para o usuário.
```
> GRANT ALL PRIVILEGES ON DATABASE simplecommercedb TO username;
```

Sair do Postegresql.
```
> \q
```

### Configuração o projeto

Abrir o arquivo `settings.py` e modificar as variável do `DATABASE` preenchendo de acordo com o usuário e senha criados no banco.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wooza_db',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': 'localhost'
    }
}
```

Rodar a migrações do projeto apontando para o novo banco de dados.
```
(venv) $ cd app/
(venv) $ python manage.py migrate
```

Rodar o projeto.
```
(venv) $ python manage.py runserver
```

## API
Url disponíveis
```
http://127.0.0.1:8000/plans/
http://127.0.0.1:8000/plans/create/
http://127.0.0.1:8000/plans/update/id
http://127.0.0.1:8000/plans/delete/id
```

## API - Criação
`[POST] http://127.0.0.1:8000/plans/create/`

Exemplo do body para criar um plano
```
{
    "plan_code": "OiPos100",
    "minutes": 100,
    "internet": "10GB",
    "price": "29.75",
    "plan_type": "Pós",
    "operator": "Oi",
    "ddds": [21]
}
```

### Validação
A API verifica se você está passando corretamente o método de requisição correta.
Caso o método de requisição seja diferente de `POST`, a API irá retornar uma mensagem de erro:
```
{
    "error": {
        "code": 400,
        "message": "Bad Request."
    }
}
```

Todos os campos são obrigatórios para a criação de um plano.
Caso alguns desses campos estejam vazios, a API irá retornar uma mensagem de erro.
```
{
    "error": {
        "code": 400,
        "message": "Bad Request.",
        "invalid_fields": [
            {
                "plan_code": "is empty."
            },
            {
                "minutes": "is empty."
            },
            {
                "internet": "is empty."
            },
            {
                "price": "is empty."
            },
            {
                "plan_type": "is empty."
            },
            {
                "operator": "is empty."
            },
            {
                "ddds": "is empty."
            }
        ]
    }
}
```

Os campos `minutes` e `price` são do tipo `int` ou `float`, mas, pode-se passar como `str`.
Caso algum desses campos estejam preenchidos erradamente, a API irá retornar uma mensagem de erro.
```
{
    "error": {
        "code": 400,
        "message": "Bad Request.",
        "invalid_fields": [
            {
                "minutes": "is not a valid number."
            },
            {
                "price": "is not a valid number."
            }
        ]
    }
}
```

Os campos `plan_type` e `ddds` já são predefinidos.
O campo `plan_type` aceita apenas os seguintes dados: `Controle, Pós e Pré`.
O campo `ddds` aceita uma lista de DDDs do Brasil, como: `[11, 21, ...]`.
Caso algum desses campos estejam preenchidos erradamente, a API irá retornar uma mensagem de erro.
```
{
    "error": {
        "code": 400,
        "message": "Bad Request.",
        "invalid_fields": [
            {
                "plan_type": "is not a valid choice."
            },
            {
                "ddds": "is not a valid choice."
            }
        ]
    }
}
```

O campo `plan_code` é único para cada plano criado.
Caso esse campo seja preenchido com algum código de plano já existente, a API irá retornar uma mensagem de erro.
```
{
    "error": {
        "code": 400,
        "message": "Bad Request.",
        "invalid_fields": [
            {
                "plan_type": "is not a valid choice."
            }
        ]
    }
}
```

### Retorno
Passado todas as validações da API, a mesma irá retornar o objeto criado.
```
{
    "data": [
        {
            "id": 1,
            "plan_code": "OiPos100",
            "minutes": 100,
            "internet": "10GB",
            "price": 29.75,
            "plan_type": "pós",
            "operator": "oi",
            "ddds": [
                21
            ]
        }
    ],
    "status_code": 200
}
```

## API - Edição
`[PUT|POST] http://127.0.0.1:8000/plans/update/<id>`

Exemplo do body para criar um plano
```
{
    "plan_code": "TimControle200",
    "minutes": 200,
    "internet": "20GB",
    "price": "59.90",
    "plan_type": "Controle",
    "operator": "Tim",
    "ddds": [11]
}
```

### Validação
Assim como a validação é feita na [API de Criação](https://github.com/assisthiago/wooza/new/master?readme=1#valida%C3%A7%C3%A3o) é feita na API de Edição.
Porém, caso um `id` seja passado e o objeto não exista na base, a API irá retornar uma mensagem de erro.
```
{
    "error": {
        "code": 404,
        "message": "Not Found."
    }
}
```

### Retorno
Passado todas as validações da API, a mesma irá retornar o objeto editado.
```
{
    "data": [
        {
            "id": 1,
            "plan_code": "TimControle200",
            "minutes": 200,
            "internet": "20GB",
            "price": 59.9,
            "plan_type": "controle",
            "operator": "tim",
            "ddds": [
                11
            ]
        }
    ],
    "status_code": 200
}
```

## API - Deleção
`[POST] http://127.0.0.1:8000/plans/delete/<id>`

### Validação
Possui apenas duas validaçãos. Verifica o método de requisição e se o `id` passado existe na base.

### Retorno
A API irá **remover** da base de dados o objeto.
Passado todas as validações da API, a mesma irá retornar o objeto deletado.
```
{
    "data": [
        {
            "id": 1,
            "plan_code": "TimControle200",
            "minutes": 200,
            "internet": "20GB",
            "price": 59.9,
            "plan_type": "controle",
            "operator": "tim",
            "ddds": [
                11
            ]
        }
    ],
    "status_code": 200
}
```

## API - Consulta
`GET http://127.0.0.1:8000/plans/`

### Retorno
```
{
    "data": [
        {
            "id": 1,
            "plan_code": "OiPos100",
            "minutes": 100,
            "internet": "10GB",
            "price": "29.75",
            "plan_type": "pós",
            "operator": "oi",
            "ddds": [
                21
            ]
        },
        {
            "id": 2,
            "plan_code": "TimControle200",
            "minutes": 200,
            "internet": "20GB",
            "price": "59.90",
            "plan_type": "controle",
            "operator": "tim",
            "ddds": [
                11
            ]
        }
    ],
    "total": 2,
    "status_code": 200
}
```

### Busca
Para fazer buscas na API de Consulta é **obrigatório** o uso de um `DDD`.
Opções disponíveis para serem adicionadas na busca dos planos:
- DDD [**obrigatório**]
- Tipo de plano
- Operador
- Código do plano

```
GET http://127.0.0.1:8000/plans/?ddds=[21]

{
    "data": [
        {
            "id": 1,
            "plan_code": "OiPos100",
            "minutes": 100,
            "internet": "10GB",
            "price": "29.75",
            "plan_type": "pós",
            "operator": "oi",
            "ddds": [
                21
            ]
        }
    ],
    "total": 1,
    "status_code": 200
}
```

**ATENÇÃO**.
A API ao buscar por uma lista de `DDDs` irá retornar apenas aquelas que tenham exatamente todos os `DDDs` iguais.
Veja o exemplo abaixo.
```
GET http://127.0.0.1:8000/plans/

{
    "data": [
        {
            "id": 1,
            "plan_code": "OiPos100",
            "minutes": 100,
            "internet": "10GB",
            "price": "29.75",
            "plan_type": "pós",
            "operator": "oi",
            "ddds": [
                11, 21, 22
            ]
        },
        {
            "id": 2,
            "plan_code": "TimControle200",
            "minutes": 200,
            "internet": "20GB",
            "price": "59.90",
            "plan_type": "controle",
            "operator": "tim",
            "ddds": [
                11
            ]
        }
    ],
    "total": 2,
    "status_code": 200
}
```

Buscando os planos que possuem o `DDD` 11.
```
GET http://127.0.0.1:8000/plans/?ddds=[11]

{
    "data": [
        {
            "id": 1,
            "plan_code": "OiPos100",
            "minutes": 100,
            "internet": "10GB",
            "price": "29.75",
            "plan_type": "pós",
            "operator": "oi",
            "ddds": [
                11, 21, 22
            ]
        },
        {
            "id": 2,
            "plan_code": "TimControle200",
            "minutes": 200,
            "internet": "20GB",
            "price": "59.90",
            "plan_type": "controle",
            "operator": "tim",
            "ddds": [
                11
            ]
        }
    ],
    "total": 2,
    "status_code": 200
}
```

Buscando os planos que possuem os `DDDs` 11 e 21.
```
GET http://127.0.0.1:8000/plans/?ddds=[11, 21]

{
    "data": [
        {
            "id": 1,
            "plan_code": "OiPos100",
            "minutes": 100,
            "internet": "10GB",
            "price": "29.75",
            "plan_type": "pós",
            "operator": "oi",
            "ddds": [
                11, 21, 22
            ]
        }
    ],
    "total": 1,
    "status_code": 200
}
```

Buscando os planos pelo `Tipo do plano`.
```
GET http://127.0.0.1:8000/plans/?ddds=[21]&plan_type=Pós

{
    "data": [
        {
            "id": 1,
            "plan_code": "OiPos100",
            "minutes": 100,
            "internet": "10GB",
            "price": "29.75",
            "plan_type": "pós",
            "operator": "oi",
            "ddds": [
                11, 21, 22
            ]
        }
    ],
    "total": 1,
    "status_code": 200
}
```

Buscando os planos pelo `Operador`.
```
GET http://127.0.0.1:8000/plans/?ddds=[21]&operator=Oi

{
    "data": [
        {
            "id": 1,
            "plan_code": "OiPos100",
            "minutes": 100,
            "internet": "10GB",
            "price": "29.75",
            "plan_type": "pós",
            "operator": "oi",
            "ddds": [
                11, 21, 22
            ]
        }
    ],
    "total": 1,
    "status_code": 200
}
```

Buscando os planos pelo `Código do plano`.
```
GET http://127.0.0.1:8000/plans/?ddds=[21]&plan_code=OiPos100

{
    "data": [
        {
            "id": 1,
            "plan_code": "OiPos100",
            "minutes": 100,
            "internet": "10GB",
            "price": "29.75",
            "plan_type": "pós",
            "operator": "oi",
            "ddds": [
                11, 21, 22
            ]
        }
    ],
    "total": 1,
    "status_code": 200
}
```
