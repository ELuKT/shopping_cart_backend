import base64
from enum import Enum, unique
from random import SystemRandom
import random
import secrets
import random
from jwcrypto import jwk

CHARACTER = ('abcdefghijklmnopqrstuvwxyz''ABCDEFGHIJKLMNOPQRSTUVWXYZ''0123456789')
def generate_state():
    return ''.join(random.choice(CHARACTER) for x in range(30))

key = jwk.JWK.generate(kty='RSA', kid=generate_state(), alg='RS256', use='sig')

print("SC_JWK:")
print(key.export_public())
print("SC_PRIVATE_KEY:")
print(base64.b64encode(key.export_to_pem(private_key=True, password=None)).decode())