import math
import random
import base64


def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def generate_prime(start=1000, end=5000):
    while True:
        num = random.randint(start, end)
        if is_prime(num):
            return num


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Обратного элемента нет")
    return (x % phi + phi) % phi


def generate_keypair(p, q):
    if not is_prime(p) or not is_prime(q):
        raise ValueError("P и Q должны быть простыми")
    if p == q:
        raise ValueError("P и Q должны быть разными")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = None
    for cand in [65537, 17, 3, 5, 7, 11, 257]:
        if 1 < cand < phi and math.gcd(cand, phi) == 1:
            e = cand
            break

    if e is None:
        for cand in range(3, phi, 2):
            if math.gcd(cand, phi) == 1:
                e = cand
                break

    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def encrypt_number(m, e, n):
    if m >= n:
        raise ValueError("m должно быть меньше n")
    return pow(m, e, n)


def decrypt_number(c, d, n):
    return pow(c, d, n)


def encrypt_text_to_base64(text, e, n):
    byte_len = (n.bit_length() + 7) // 8
    cipher_bytes = bytearray()
    for ch in text:
        m = ord(ch)
        if m >= n:
            raise ValueError("Символ не помещается в модуль n")
        c = pow(m, e, n)
        cipher_bytes.extend(c.to_bytes(byte_len, "big"))
    return base64.b64encode(cipher_bytes).decode("ascii")


def decrypt_text_from_base64(b64_string, d, n):
    byte_len = (n.bit_length() + 7) // 8
    cipher_bytes = base64.b64decode(b64_string)
    chars = []
    for i in range(0, len(cipher_bytes), byte_len):
        block = cipher_bytes[i:i + byte_len]
        c = int.from_bytes(block, "big")
        chars.append(chr(pow(c, d, n)))
    return "".join(chars)


def main():
    mode = input("Сгенерировать P и Q автоматически? (y/n): ").strip().lower()

    if mode == "n":
        p = int(input("Введите P: "))
        q = int(input("Введите Q: "))
    else:
        p = generate_prime(1500, 4000)
        q = generate_prime(1500, 4000)
        while q == p:
            q = generate_prime(1500, 4000)
        print(f"Сгенерированы: P = {p}, Q = {q}")

    print(f"P простое: {is_prime(p)}")
    print(f"Q простое: {is_prime(q)}")

    if not is_prime(p) or not is_prime(q):
        print("Ошибка: одно из чисел не простое")
        return

    (e, n), (d, _) = generate_keypair(p, q)
    phi = (p - 1) * (q - 1)

    print(f"n = {n}")
    print(f"phi = {phi}")
    print(f"Открытый ключ: ({e}, {n})")
    print(f"Закрытый ключ: ({d}, {n})")

    m_input = input(f"Введите число m (или Enter для 42): ").strip()
    m = int(m_input) if m_input else 42

    c = encrypt_number(m, e, n)
    decrypted_m = decrypt_number(c, d, n)

    print(f"Исходное число: {m}")
    print(f"Зашифрованное число: {c}")
    print(f"Расшифрованное число: {decrypted_m}")
    print(f"Числа совпали: {m == decrypted_m}")

    text_input = input("Введите текст (или Enter для теста): ").strip()
    text = text_input if text_input else "Привет, RSA!"

    b64_cipher = encrypt_text_to_base64(text, e, n)
    decrypted_text = decrypt_text_from_base64(b64_cipher, d, n)

    print(f"Исходный текст: {text}")
    print(f"Зашифрованный (Base64): {b64_cipher}")
    print(f"Расшифрованный текст: {decrypted_text}")
    print(f"Текст совпал: {text == decrypted_text}")


if __name__ == "__main__":
    main()
