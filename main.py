import random

import numpy as np


def adamar(n):  # N = 2^n - dimensionality
    H = [[0] * (2 ** n) for i in range(2 ** n)]
    # h = (1 / 2) ** (n / 2)
    N = 2 ** n
    k = 2
    H[0][0] = 1

    while k <= N:
        for i in range(k):
            for j in range(k):
                if (i < k / 2) & (j < k / 2):
                    pass
                else:
                    if (i >= k / 2) & (j >= k / 2):
                        H[i][j] = -(H[i - k // 2][j - k // 2])
                    else:
                        if i > j:
                            H[i][j] = H[i - k // 2][j]
                        else:
                            H[i][j] = H[i][j - k // 2]
        k = k * 2

    return H


def encode(binstr, block_size):
    to_encode = list()
    for i in range(0, len(binstr), block_size):
        to_encode.append(binstr[i:i + block_size])
    if len(to_encode[-1]) < block_size:
        k = block_size - len(to_encode[-1])
        to_encode[-1] = to_encode[-1] + '0' * k

    adamar_matrix = adamar(block_size)
    encoded_seq = ""

    for i in range(len(to_encode)):
        position = int(to_encode[i], 2)
        encoded_seq += "".join(str((x + 1) // 2) for x in adamar_matrix[position])

    return encoded_seq


def get_error_vector(encoded, block_size):
    to_decode = list()
    for bit in encoded:
        if int(bit) == 0:
            to_decode.append(-1)
        else:
            to_decode.append(1)
    adamar_matrix = np.asmatrix(adamar(block_size))
    encoded_vector = np.asmatrix(to_decode)
    F = np.matmul(encoded_vector, adamar_matrix)
    return F


def make_error(message, n):
    errors = list()

    for i in range(n):
        error_position = random.randrange(len(res))
        while (errors.count(error_position) > 0):
            error_position = random.randrange(len(res))
        errors.append(error_position)

        if res[error_position] == '0':
            error_str = message[:error_position] + "1" + message[error_position + 1:]
        else:
            error_str = message[:error_position] + "0" + message[error_position + 1:]
        print("Место ошибки: ", error_position + 1)
        message = error_str

    print("Сообщение с ошибкой", error_str)
    return error_str


def correct_error(error_vector, block_size):
    max = 0
    for i in range(len(error_vector.tolist()[0])):
        if abs(error_vector.tolist()[0][i]) > max:
            max = error_vector.tolist()[0][i]
            indexof_max = i
    if max == 2 ** block_size:
        print("Ошибок в сегменте нет")
    else:
        print("Количество ошибок в сегменте: ", (2 ** block_size - max) // 2)
        print("Оригинальный сегмент: ", encode(bin(indexof_max)[2:], block_size))
    msg = bin(indexof_max)[2:]
    return msg


def correct(message, block_size):
    to_decode = list()
    corrected = ""
    for i in range(0, len(message), 2 ** block_size):
        to_decode.append(message[i:i + 2 ** block_size])
    for i in range(len(to_decode)):
        print(f'Проверяем сегмент {to_decode[i]} под номером {i + 1}: ')
        error_vector = get_error_vector(to_decode[i], block_size)
        corrected += correct_error(error_vector, block_size)
    return corrected


for i in range(int(input("Введите длину для генерации кодируемой последовательности: "))):
    print(random.randrange(2), end="")
print()
binarystr = input("Введите строку для кодирования: ")
block_size = int(input("Введите n (длину блока последовательности): "))
error_count = int(input("Введите число ошибок: "))

res = encode(binarystr, block_size)

print("Закодированное сообщение: ", res)
error_message = make_error(res, error_count)

print("Оригинальное сообщение:", correct(error_message, block_size))
