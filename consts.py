ENCODED_LENGTH = 27
R = 5
UNCODED_LENGTH = ENCODED_LENGTH - R
R_MATRIX = [
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
UNCODED_LENGTH_BYTES = 11
UNCODED_LENGTH_BITS = UNCODED_LENGTH_BYTES * 8
UNCODED_MSGS_PER_BATCH = 4  # читаем 88 бит = 4 слова по 22 бита = 11 байт
ENCODED_MSGS_PER_BATCH = 8  # получаем 216 бит = 8 слов по 27 бит = 27 байт
ENCODED_LENGTH_BITS = ENCODED_LENGTH * ENCODED_MSGS_PER_BATCH
READ_FOR_SENDING = int(ENCODED_MSGS_PER_BATCH / UNCODED_MSGS_PER_BATCH)

ERROR = 2
