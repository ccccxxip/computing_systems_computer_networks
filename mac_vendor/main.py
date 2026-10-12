import os
import re

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mac-vendor.txt')

MAC_PATTERN = re.compile(r'^[0-9A-F]{2}([-:])(?:[0-9A-F]{2}\1){4}[0-9A-F]{2}$')


def load_vendors(file_name):
    vendors = {}
    with open(file_name, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            prefix, name = line.split('\t', 1)
            vendors[prefix.upper()] = ' '.join(name.split())
    return vendors


def find_vendor(mac, vendors):
    prefix = mac.upper()[:8].replace('-', '').replace(':', '')
    return vendors.get(prefix)


vendors = load_vendors(FILE_NAME)

while True:
    mac = input('Введите MAC-адрес в формате F0-79-59-70-A7-20: ').strip().upper()
    if MAC_PATTERN.match(mac):
        break
    print('Неверный формат, попробуйте ещё раз')

vendor = find_vendor(mac, vendors)
if vendor:
    print('Производитель:', vendor)
else:
    print('Производитель не найден: префикса', mac[:8], 'нет в списке')