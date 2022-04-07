import socket
import time
import datetime
from utils import *
import zlib
import random

if __name__ == '__main__':
    sock = socket.socket()

    time.sleep(1)

    sock.connect(('192.168.1.50', 9090))

    with open("host1.txt", "a", encoding='utf-8') as log:
        log.write('Connection established\nTime {time}\nReceiver address: {receiver}\nSender address (this): {sender}\n'.format(
            time=datetime.datetime.now(),
            receiver=sock.getpeername(),
            sender=sock.getsockname()
        ))
        log.write('------------------------------\n')

        whole_message = bytearray()
        with open("msg.txt", "rb") as file_in, open("msg.hem", "wb") as file_out:
            byte = bytearray(file_in.read(UNCODED_LENGTH_BYTES))
            buffer = None
            while byte:
                for z in range(0, READ_FOR_SENDING):
                    whole_message += byte
                    log.write('Read batch of {n} messages\n'.format(n=UNCODED_MSGS_PER_BATCH))
                    if UNCODED_LENGTH_BYTES != len(byte):
                        log.write('Read last message, adding {n} missing bits\n'.format(n=(UNCODED_LENGTH_BYTES - len(byte)) * 8))
                    bits = [0] * UNCODED_LENGTH_BITS
                    bytes_to_bits(bits, byte)
                    log.write('Bits of the batch: {bits}\n'.format(bits=bits))
                    for k in range(0, UNCODED_MSGS_PER_BATCH):
                        message = bits[k * UNCODED_LENGTH:(k + 1) * UNCODED_LENGTH]
                        log.write('Message {i} of {n}: {bits}\n'.format(i=k + 1, n=UNCODED_MSGS_PER_BATCH, bits=message))
                        for i in range(0, R):
                            pos = 2 ** i - 1
                            message[pos:pos] = [0]
                        hamming(message)
                        if ERROR == 1:
                            if random.random() > 0.5:
                                make_error(message, log)
                        elif ERROR == 2:
                            rnd = random.random()
                            if rnd > 0.75:
                                make_error(message, log)
                            if rnd > 0.5:
                                make_error(message, log)
                        log.write('After adding control bits: {bits}\n'.format(bits=message))
                        if z == 0 and k == 0:
                            buffer = message
                        else:
                            buffer += message
                        log.write('Adding to buffer...\n')
                    byte = bytearray(file_in.read(UNCODED_LENGTH_BYTES))
                    log.write('')
                final_bytes = [0] * ENCODED_LENGTH
                bits_to_bytes(buffer, final_bytes)
                log.write('Buffer is full, sending...\n\n')
                final_bytes = bytearray(final_bytes)
                sock.send(final_bytes)
                file_out.write(final_bytes)

        log.write('Whole message that was sent:\n{text}\n\n'.format(text=whole_message.decode()))
        crc32 = hex(zlib.crc32(whole_message) & 0xffffffff)
        with open("msg.crc32", "w") as file_out:
            file_out.write(crc32)
        log.write('CRC32: {hash}\n\n'.format(hash=crc32))

        sock.send(bytes([0]))
        result = sock.recv(1024)
        log.write(result.decode() + '\n')
        log.write('------------------------------\nEnd of transmission\n\n')

    sock.close()
