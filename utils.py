from consts import *
from random import randrange


def bytes_to_bits(bit_array, byte_array):
    for i in range(0, len(byte_array)):
        for j in range(0, 8):
            if byte_array[i] & (2 ** j) != 0:
                bit_array[i * 8 + 7 - j] = 1
            else:
                bit_array[i * 8 + 7 - j] = 0


def bits_to_bytes(bit_array, byte_array):
    for i in range(0, len(byte_array)):
        cur_byte = 0
        for j in range(0, 8):
            cur_byte += (2 ** j) * bit_array[i * 8 + 7 - j]
        byte_array[i] = cur_byte


def make_error(message, log):
    pos = randrange(len(message))
    cur = message[pos]
    if cur == 1:
        message[pos] = 0
    else:
        message[pos] = 1
    log.write('Making error at {x}th position\n'.format(x=pos))


def hamming(message):
    rs = [0] * R
    for i in range(0, R):
        r_sum = 0
        for j in range(0, ENCODED_LENGTH):
            r_sum += R_MATRIX[i][j] * message[j]
        rs[i] = r_sum % 2
    for i in range(0, R):
        pos = 2 ** i - 1
        message[pos] = rs[i]
