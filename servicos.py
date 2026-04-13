# Mapeamento de portas conhecidas // Mapping of known ports

COMMON_PORTS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB",
}

def get_servico(port: int) -> str:                              # Recebe número inteiro e retorna uma string
    """Retorna o nome do serviço ou 'Desconhecido' para portas não mapeadas."""
    return COMMON_PORTS.get(port, "Desconhecido")    # Através do método .get, assimila o valor de "port: int" à lista de COMMON_PORTS ou retorna o valor default após a vírgula 