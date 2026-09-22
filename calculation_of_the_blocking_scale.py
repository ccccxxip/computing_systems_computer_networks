import ipaddress

def calculate_blocked_space(filename):
    total_ips = 0
    total_networks = 0

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            net = ipaddress.ip_network(line)
            
            total_ips += net.num_addresses
            total_networks += 1

    return total_networks, total_ips

if __name__ == '__main__':
    file_path = 'blocked-networks.txt'
    networks_count, total_ips_count = calculate_blocked_space(file_path)

    print(f"всего адресов: {networks_count}")
    print(f"количество заблокированных: {total_ips_count:,}".replace(',', ' '))