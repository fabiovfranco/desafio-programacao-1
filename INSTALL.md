# Guia de instalação

## Pré requisitos
> - Python 2.7.x
> - Pip (https://pip.pypa.io/en/latest/installing.html)
> - Virtualenv (https://virtualenv.pypa.io/en/latest/)

## Configuração do ambiente
### Crie um ambiente virutal para a aplicação:
```
  $ mkdir <ambiente_virtual>
  $ virtualenv <ambiente_virtual>
```

### Insale os componentes da aplicação
```
  $ source <ambiente_virtual>/bin/activate
  $ <ambiente_virtual>/bin/pip install Django==1.8
```

### Prepare a aplicação. 
Exeucte os comandos abaixo na pasta src da aplicação
```
  $ cd <pasta_src_aplicação>
  $ <ambiente_virtual>/bin/python manage.py migrate
  $ <ambiente_virtual>/bin/python manage.py cratesuperuser
```

### Criar pasta de upload de arquivos:
```
  $ mkdir -p /opt/import/files
```

### Inicialação do servidor
```
  $ cd <pasta_src_aplicação>
  $ <ambiente_virtual>/bin/python manage.py runserver localhost:8000
```

> Para fazer upload de arquivos utilize a url abaixo:
http://localhost:8000

> Para visualizar o conteúdo importado utilize a url:
http://localhost:8000/admin
	
