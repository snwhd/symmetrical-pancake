#!/usr/bin/env python3
from Crypto.Cipher import AES
import base64
import inspect
import marshal
import typing
import zlib

import level_one
import level_two


def encrypt_level(
    level: typing.Callable[[], str],
    password: str,
) -> bytes:
    while len(password) < 32:
        password += 'a'

    # compile & serialize
    codedata = marshal.dumps(level.__code__)

    # compress
    compressed = zlib.compress(codedata)
    padding = 16 - (len(compressed) % 16)
    compressed += bytes([padding])*padding

    # encrypt
    aes = AES.new(password, AES.MODE_CBC, '1234567890123456')
    encrypted = aes.encrypt(compressed)

    # encode
    return base64.b64encode(encrypted)


def decrypt_level(
    encoded: bytes,
    password: str,
) -> 'code':
    while len(password) < 32:
        password += 'a'

    # decode
    data = base64.b64decode(encoded)

    # decrypt
    aes = AES.new(password, AES.MODE_CBC, '1234567890123456')
    decrypted = aes.decrypt(data)
    compressed = decrypted[:-decrypted[-1]]

    # decompress
    codedata = zlib.decompress(compressed)

    # deserialize
    return marshal.loads(codedata)


if __name__ == '__main__':
    levels = [
        level_one,
        level_two,
    ]


    with open('game.py', 'w') as f:
        f.write(f'''\
#!/usr/bin/env python3
from Crypto.Cipher import AES
import base64
import marshal
import zlib


{inspect.getsource(decrypt_level)}


LEVELS = [
''')

        password = 'begin'
        for level in levels:
            blob = encrypt_level(level.level, password)
            password = level.EXPECTED_ANSWER
            f.write(f'    {blob},\n')

        f.write('''\
]


if __name__ == '__main__':
    password = 'begin'
    for i, level in enumerate(LEVELS):
        func = decrypt_level(level, password)
        password = eval(func)

    print('goodbye')
''')

    # func = decrypt_level(blob, level_one.EXPECTED_ANSWER)
    # m = exec(func)
