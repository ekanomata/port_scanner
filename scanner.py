# Scaneamento de ports com sockets

import socket
import argparse
import concurrent.futures
import datetime
from servicos import get_servico



TIMEOUT   = 0.5                                         # Segundos de espera por porta
MAX_WORKERS = 100                                       # Threads simultâneas


def resolve_host(host: str) -> str:                     # Utilização da biblioteca socket para manipulação entre hostnames e enereços IPs, além de verificação de erro
    """Resolve hostname para IP e valida o alvo."""
    try:
        ip = socket.gethostbyname(host)                 # Função gethostbyname transforma hostname em um endereço IP
        print(f"\n🟦 Alvo  : {host}")
        print(f"🟦 IP    : {ip}")
        print(f"🟦 Início: {datetime.datetime.now()}\n")
        return ip
    except socket.gaierror:                             # Verificação de Erro
        print(f"🟥 Erro: não foi possível resolver '{host}'")
        raise SystemExit(1)


def grab_banner(ip: str, port: int) -> str:             # 
    """Tenta capturar o banner do serviço (primeiros 128 bytes)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((ip, port))
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(128).decode("utf-8", errors="ignore").strip()
            return banner.split("\n")[0]
    except:
        return ""


def scan_port(ip: str, port: int) -> dict | None:       # Função à base de connect_ex(), retornando 0 para port abertas
    """Tenta conectar à porta. Retorna dict se aberta, None se fechada."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            result = s.connect_ex((ip, port))
            if result == 0:                             # Caso a port esteja aberta, cria uma biblioteca com os dados
                service = get_servico(port)
                banner  = grab_banner(ip, port)
                return {"port": port, "service": service, "banner": banner}
    except socket.error:
        pass                                            # Error handling
    return None


def run_scan(ip: str, start: int, end: int) -> list:    # Utilização de ThreadPoolExecutor para testar várias portas ao mesmo tempo, evitando demora durante a execução do scan
    """Escaneia o range de portas usando múltiplas threads."""
    open_ports = []
    total = end - start + 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        chaves = {pool.submit(scan_port, ip, p): p for p in range(start, end + 1)}

        for i, future in enumerate(concurrent.futures.as_completed(chaves), 1):
                                                        # Brra de progresso
            pct = int((i / total) * 40)
            bar = "🟩" * pct + "⬜" * (40 - pct)
            print(f"\r[{bar}] {i}/{total}", end="", flush=True)

            result = future.result()
            if result:
                open_ports.append(result)

    print()                                             
    return sorted(open_ports, key=lambda x: x["port"])


def print_results(open_ports: list):
    """Exibe os resultados formatados no terminal."""
    print(f"\n{'─'*48}")
    print(f"{'PORTA':<8} {'SERVIÇO':<15} {'BANNER'}")   # :<8 e :<15 para formatação 
    print(f"{'─'*48}")
    if not open_ports:
        print("Nenhuma porta aberta encontrada.")
    else:
        for p in open_ports:
            banner = (p['banner'][:35] + "…") if len(p['banner']) > 35 else p['banner'] 
            print(f"{p['port']:<8} {p['service']:<15} {banner}")
    print(f"{'─'*48}")
    print(f"Total: {len(open_ports)} porta(s) aberta(s)\n")


def save_report(host: str, ip: str, open_ports: list):  # Gera um nome de arquivo único usando timestamp
    """Salva relatório em arquivo .txt."""
    filename = f"scan_{host}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(f"Relatório de scan — {host} ({ip})\n")
        f.write(f"Data: {datetime.datetime.now()}\n\n")
        for p in open_ports:
            f.write(f"Porta {p['port']:5} | {p['service']:15} | {p['banner']}\n")
    print(f"🟦 Relatório salvo em: {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port Scanner simples")
    parser.add_argument("host",           help="Alvo (hostname ou IP)")
    parser.add_argument("-s", "--start",  type=int, default=1,     help="Porta inicial")
    parser.add_argument("-e", "--end",    type=int, default=1024,  help="Porta final")
    parser.add_argument("-r", "--report", action="store_true",      help="Salvar relatório")
    args = parser.parse_args()

    ip = resolve_host(args.host)
    open_ports = run_scan(ip, args.start, args.end)
    print_results(open_ports)

    if args.report:
        save_report(args.host, ip, open_ports)