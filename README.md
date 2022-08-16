# Requisitos

Python 3.10.6 e bibliotecas descritas no "requirements.txt".

Sugestão de instação:

1) Instale [pyenv](https://github.com/pyenv/pyenv) para gerenciar versões do Python.
2) Após instalar  `pyenv`, instale Python 3.10.6 executando o seguinte comando no terminal: `CONFIGURE_OPTS="--enable-optimizations --with-lto" pyenv install 3.10.6` 
3) Após instalar o Python 3.10.6, navegue até o diretório raiz do repositório e defina o "Python padrão para este repositório" com o comando: `pyenv local 3.10.6`
4) Ainda no diretório raiz do repositório, crie um ambiente (para instalação de bibliotecas do Python) com o seguinte comando: `python -m venv .venv`
5) Ainda no diretório raiz do repositório, active o ambiente criado na etapa anterior com o seguinte comando: `source .venv/bin/activate`.  
6) Ainda no diretório raiz do repositório, instale as bibliotecas enumeradas no arquivo `requirements.txt` usando o comando `pip install -r requirements.txt`

Observação importante: toda vez que você for utilizar esse ambiente, isto é, esse conjunto de bibliotecas, é necessário repetir a etapa 5 (ativação do ambiente). Os efeitos dessa "ativação de ambiente" persistem apenas até o terminal ser fechado.
