🔍 Port Scanner

Port scanner de linha de comando desenvolvido em Python com utilização da bibliotea socket

Funcionalidades:
- Escaneamento de ranges de portas com multithreading (ThreadPoolExecutor)
- Identificação de serviços conhecidos (HTTP, SSH, FTP...)
- Banner grabbing básico para fingerprinting de serviços
- Geração de relatório em .txt (-r ou --report)

Como usar:
$ python scanner.py  [-s porta_inicial] [-e porta_final] [-r]
