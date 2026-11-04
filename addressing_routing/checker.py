import os
import re
import socket


def load_registry(filepath="addressing_routing/register.txt"):
    if not os.path.exists(filepath):
        filepath = "register.txt"

    urls = set()
    domains = set()
    ips = set()

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.strip().split(";")
            if len(parts) >= 4:
                if parts[1]:
                    urls.update(u.strip() for u in parts[1].split(",") if u.strip())
                if parts[2]:
                    domains.update(d.strip().lower() for d in parts[2].split(",") if d.strip())
                if parts[3]:
                    ips.update(ip.strip() for ip in parts[3].split(",") if ip.strip())

    return urls, domains, ips


def extract_domain(url):
    match = re.search(r"^(?:https?://)?([^/:]+)", url)
    return match.group(1).lower() if match else url.lower()


def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None


def check_url(url, urls, domains, ips):
    url = url.strip()
    domain = extract_domain(url)
    ip = resolve_ip(domain)

    url_blocked = url in urls or url.rstrip("/") in urls
    domain_blocked = domain in domains
    ip_blocked = ip in ips if ip else False

    print(f"URL:   {url} -> {'заблокирован' if url_blocked else 'не найден'}")
    print(f"Домен: {domain} -> {'заблокирован' if domain_blocked else 'не найден'}")
    print(f"IP:    {ip or 'не определен'} -> {'заблокирован' if ip_blocked else 'не найден'}")

    if url_blocked or domain_blocked or ip_blocked:
        print("заблокирован")
    else:
        print("доступен")


def main():
    urls, domains, ips = load_registry()
    print(f"База загружена ({len(urls)} URL, {len(domains)} доменов, {len(ips)} IP)\n")

    while True:
        url = input("Введите URL (или 'exit'): ").strip()
        if not url:
            continue
        if url.lower() in ("exit", "quit", "q"):
            break
        check_url(url, urls, domains, ips)


if __name__ == "__main__":
    main()

