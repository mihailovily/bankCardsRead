from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES 
import secrets

def generate_visa_pvv(card_number, pin, pvki):
    # Вычисляем TSP = PAN11 + PVKI + PIN
    pan11 = format(int(card_number[-11:], 10), '011b')  # двоичное представление последних 11 цифр номера карты
    pvki_binary = format(pvki, '04b')  # двоичное представление PVKI
    pin_binary = format(pin, '04b')  # двоичное представление PIN
    tsp = pan11 + pvki_binary + pin_binary

    # Преобразуем tsp в байты
    tsp_bytes = bytes(tsp, 'utf-8')

    # Получаем пару ключей Key A, Key B
    key_a, key_b = generate_keys(pvki)

    # Вычисляем Result = EncryptDES(Key A, DecryptDES(Key B, EncryptDES(Key A, TSP)))
    encrypted_tsp = encrypt_des(key_a, tsp_bytes)
    decrypted_tsp = decrypt_des(key_b, bytes.fromhex(encrypted_tsp))
    result = encrypt_des(key_a, decrypted_tsp)

    # Двухпроходная десятичная декомпозиция значения Result
    result_digits = []
    for digit in result:
        result_digits.extend(divmod(int(digit, 16), 10))  # Убираем вычитание 10

    # Значение PVV равно первым четырем цифрам полученного результата
    pvv = ''.join(map(str, result_digits[:4]))

    return pvv

def generate_keys(pvki):
    # Случайным образом генерируем ключи Key A, Key B
    key_a = secrets.token_bytes(8)
    key_b = secrets.token_bytes(8)

    return key_a, key_b

def encrypt_des(key, data):
    # Используем актуальную версию TripleDES
    cipher = Cipher(TripleDES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # Выравнивание данных перед шифрованием
    padder = padding.PKCS7(TripleDES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data.hex().upper()

def decrypt_des(key, data):
    # Используем актуальную версию TripleDES
    cipher = Cipher(TripleDES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()
    return decrypted_data

# Пример использования
card_number = "****"  # Пример номера карты
pvki = 1  # Пример PVKI
true_pvv = ****
for i in range(10000):
    pvv = generate_visa_pvv(card_number, i, pvki)
    print(pvv)

print(pvv)

