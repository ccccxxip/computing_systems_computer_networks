import os
import json
import lzma
import random
import socket
import urllib.request
from typing import List

REGISTRY_PATH = "blocked_domains/domains.xz"
SAMPLE_SIZE = 50
RANDOM_SEED = 42
OUT_REGISTRY = "blocked_domains/used_registry_sample.txt"
OUT_AVAILABLE = "blocked_domains/available_domains.txt"


def load_ru_domains(filepath: str) -> List[str]:
    with lzma.open(filepath, "rt", encoding="utf-8", errors="ignore") as f:
        data = json.load(f)

    ru_domains = set()
    for item in data:
        dom = item.strip("\"' \t\r\n").lower()
        if dom.endswith(".ru") and dom.count(".") == 1 and not dom.startswith("*"):
            ru_domains.add(dom)

    return sorted(list(ru_domains))


def check_dns(domain: str) -> bool:
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False


def check_whois(domain: str) -> str:
    url = f"http://api.whois.vu/?q={domain}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            if res.get("available") == "yes":
                return "AVAILABLE"
            return "REGISTERED"
    except Exception:
        try:
            s = socket.create_connection(("whois.tcinet.ru", 43), timeout=3)
            s.sendall(f"{domain}\r\n".encode())
            reply = s.recv(2048).decode(errors="ignore")
            s.close()
            if "No entries found" in reply:
                return "AVAILABLE"
            elif "state:" in reply or "domain:" in reply:
                return "REGISTERED"
        except Exception:
            pass
        return "ERROR"


def main():
    all_domains = load_ru_domains(REGISTRY_PATH)
    print(f"Найдено уникальных .ru доменов: {len(all_domains)}")

    random.seed(RANDOM_SEED)
    sample = random.sample(all_domains, SAMPLE_SIZE)
    print(f"кол-во случайных {len(sample)} доменов для проверки")

    with open(OUT_REGISTRY, "w", encoding="utf-8") as f:
        for d in sample:
            f.write(f"{d}\n")
    print(f"Сохранили выборку в {OUT_REGISTRY}\n")

    available_list = []
    registered_count = 0
    error_count = 0

    for dom in sample:
        if check_dns(dom):
            registered_count += 1
            print(f"{dom} - занят (отвечает DNS)")
            continue

        status = check_whois(dom)
        if status == "AVAILABLE":
            print(f"{dom} - СВОБОДЕН")
            available_list.append(dom)
        elif status == "REGISTERED":
            print(f"{dom} - занят (по whois)")
            registered_count += 1
        else:
            print(f"{dom} - ошибка при проверке")
            error_count += 1

    print(f"Проверено доменов: {len(sample)}")
    print(f"Свободных: {len(available_list)}")
    print(f"Занятых: {registered_count}")
    print(f"Ошибок: {error_count}")

    with open(OUT_AVAILABLE, "w", encoding="utf-8") as f:
        for dom in available_list:
            f.write(f"Домен: {dom}\n")
            f.write(f"Статус: Свободен (available=yes)\n")
            f.write(f"Ссылка: https://whois.ru/{dom}\n\n")

    print(f"\nСвободные домены записали в {OUT_AVAILABLE}")


if __name__ == "__main__":
    main()
