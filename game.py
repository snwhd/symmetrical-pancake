#!/usr/bin/env python3
from Crypto.Cipher import AES
import base64
import marshal
import zlib


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



LEVELS = [
    b'+c9uKe6TNjaX6ha/LAnG4nBpeUua1FXoacrxxyf16CLgoovriETj+me4+QA3q2PsCvTKMrCqZivfycTjZpgpXz6SdZOfALHWqsF4oQPJfjD+OJzefAk/kBRrHXdy8G5xAI+acE2Z3KA/Q4j+JOTP/s2G8kwvwQ9zzCV54Vgvmw0OvHy5u/bAXnT/iJwHDB1plVOl138R32XcO84Sqe3Uszl7ScNET7SBXeeTczaUILLkk9fYD3wTB+vRpWTiaDepCGttbjNgD7plIkM6anQDFcNLLkWm5TLO7IClUSDBpSI=',
    b'HgTC5ptHoZCvcuyIDBtfCSeIHXGMiNCaAPzyMo8oShW57yg77BKD6Yr9EnRmoVdrU/lSAjzldrVSdT7OMdEmcVwyzUT2KwjWc9yjKpF71lpwy9WYhJ6tDG0YuXKwQUafPvcz1f/SFiKUOi0PQKeXX/HLnTL5lm1t12I3pO6RqQOfgXt3NSWIWwrehCwGqY5i',
]


if __name__ == '__main__':
    password = 'begin'
    for i, level in enumerate(LEVELS):
        func = decrypt_level(level, password)
        password = eval(func)

    print('goodbye')
