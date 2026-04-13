##  🔍 Port Scanner 

Port scanner de linha de comando desenvolvido em Python com utilização da biblioteca socket

Funcionalidades:
- Escaneamento de ranges de portas com multithreading (ThreadPoolExecutor)
- Identificação de serviços conhecidos (HTTP, SSH, FTP...)
- Banner grabbing básico para fingerprinting de serviços
- Geração de relatório em .txt (-r ou --report)

##
Como baixar / Download:

**1. Clonar repositório público desse Github no terminal**

`git clone https://github.com/ekanomata/port_scanner.git`

**2. Entrar na pasta do projeto**

`cd Port Scanner`

**3. Utilização do scanner**

`python scanner.py [-s porta inicial] [-e porta final] [-r]`

## 
Funções / Usage

`-r` ou `--report` -> Cria um arquivo .txt de relatório das portas abertas

`-s` ou `--start`  -> Define a porta inicial em que o scan começará

`-e` ou `--end`    -> Define a porta final em que o scan parará
