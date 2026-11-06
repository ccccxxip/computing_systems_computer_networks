import sys
import webbrowser

DOMAINS = [
    "ters-casino.ru",
    "caeko-profi.ru",
    "hosterplus.ru"
]

def main():
    service = sys.argv[1].lower() if len(sys.argv) > 1 else "whois"
    
    print(f"[*] Открываем выбранные домены на {service.upper()}...")
    for dom in DOMAINS:
        if service == "reg":
            url = f"https://www.reg.ru/buy/domain/?domains={dom}"
        elif service == "nic":
            url = f"https://www.nic.ru/search/domain/?searchWord={dom}"
        else:
            url = f"https://whois.ru/{dom}"
            
        print(f"  -> {dom}: {url}")
        webbrowser.open(url)

if __name__ == "__main__":
    main()
