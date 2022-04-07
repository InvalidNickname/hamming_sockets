import socket
import datetime
from utils import *
import zlib

if __name__ == "__main__":
    sock = socket.socket()
    sock.bind(('192.168.1.50', 9090))
    sock.listen(1)
    conn, address = sock.accept()

    with open("host2.txt", "a", encoding='utf-8') as log:
        log.write('Connection established\nTime {time}\nReceiver address (this): {receiver}\nSender address: {sender}\n'.format(
            time=datetime.datetime.now(),
            receiver=sock.getsockname(),
            sender=address
        ))
        log.write('------------------------------\n')

        broken = False
        errors_fixed = 0
        correct_words = 0
        wrong_words = 0

        whole_message = bytearray()
        data = None
        while True:
            data = conn.recv(int(ENCODED_LENGTH_BITS / 8))
            if not data or data == bytes([0]):
                break
            log.write('Received batch of {n} messages: {text}\n'.format(n=int(len(data) * 8 / ENCODED_LENGTH), text=list(data)))
            bits = [0] * ENCODED_LENGTH_BITS
            bytes_to_bits(bits, data)
            buffer = None
            for k in range(0, ENCODED_MSGS_PER_BATCH):
                message = bits[k * ENCODED_LENGTH:(k + 1) * ENCODED_LENGTH]
                log.write('Message {n} of {m}: {text}\n'.format(n=k, m=ENCODED_MSGS_PER_BATCH, text=message))
                hamming(message)
                syndrome = [0] * R
                for i in range(0, R):
                    pos = 2 ** i - 1
                    syndrome[i] = message[pos]
                syndrome_value = 0
                for i in range(0, R):
                    syndrome_value += (2 ** i) * syndrome[i]
                if syndrome_value == 0:
                    log.write('Syndrome equals 0, no errors\n')
                    correct_words += 1
                else:
                    wrong_words += 1
                    syndrome_value -= 1
                    if syndrome_value >= len(message):
                        log.write('More than 1 error detected, message is irrestorable\n')
                        broken = True
                    else:
                        log.write('Error in {x}th bit, fixing\n'.format(x=syndrome_value))
                        if message[syndrome_value] == 1:
                            message[syndrome_value] = 0
                        else:
                            message[syndrome_value] = 1
                        log.write('Fixed: {text}\n'.format(text=message))
                        errors_fixed += 1
                for i in reversed(range(0, R)):
                    pos = 2 ** i - 1
                    del message[pos]
                log.write('Message after deleting control bits: {text}\n'.format(text=message))
                if k == 0:
                    buffer = message
                else:
                    buffer += message
            log.write('Batch received and decoded\n\n')
            if not broken:
                final_bytes = [0] * UNCODED_LENGTH
                bits_to_bytes(buffer, final_bytes)
                whole_message += bytearray(final_bytes)

        if not broken:
            log.write('Deleting trailing zeros...\n\n')
            for i in reversed(range(0, len(whole_message))):
                if whole_message[i] == 0:
                    del whole_message[i]
                else:
                    break
            log.write('Decoded message:\n{text}\n\n'.format(text=whole_message.decode()))
            log.write('CRC32: {hash}\n'.format(hash=hex(zlib.crc32(whole_message) & 0xffffffff)))
        else:
            log.write('More than 1 error per message detected, restoration is impossible')

        conn.send('Correct: {x}\nWrong: {y}\nFixed: {z}'.format(x=correct_words, y=wrong_words, z=errors_fixed).encode())
        log.write('------------------------------\nEnd of transmission\n\n')

    conn.close()
