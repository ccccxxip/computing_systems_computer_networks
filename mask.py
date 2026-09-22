def get_netmask(prefix):
    if prefix < 0 or prefix > 32:
        return "ошибка: префикс должен быть от 0 до 32"

    binary_mask = "1" * prefix + "0" * (32 - prefix)

    b1 = binary_mask[0:8]
    b2 = binary_mask[8:16]
    b3 = binary_mask[16:24]
    b4 = binary_mask[24:32]

    o1 = int(b1, 2)
    o2 = int(b2, 2)
    o3 = int(b3, 2)
    o4 = int(b4, 2)

    return f"{o1}.{o2}.{o3}.{o4}"


if __name__ == "__main__":
    p = int(input("введите префикс сети: "))
    mask = get_netmask(p)
    print(f"маска подсети для /{p}: {mask}")