from prime_gen import get_prime
import random
from math import lcm, gcd
import base64


class RSAPublicKey:
    def __init__(self, n: int, e: int):
        """
        RSAPublicKey ::= SEQUENCE {
             modulus           INTEGER,  -- n
             publicExponent    INTEGER   -- e
        }
        """
        self.modulus = n
        self.publicExponent = e

    def __repr__(self) -> str:
        seq = "RSAPublicKey ::= {\n"
        for name, value in vars(self).items():
            seq += f"\t{name}:\t{value}\n"
        seq += "}"
        return seq


class RSAPrivateKey:
    def __init__(self, n: int, e: int, d: int, p: int, q: int):
        """
        RSAPrivateKey ::= SEQUENCE {
             version           Version,
             modulus           INTEGER,  -- n
             publicExponent    INTEGER,  -- e
             privateExponent   INTEGER,  -- d
             prime1            INTEGER,  -- p
             prime2            INTEGER,  -- q
             exponent1         INTEGER,  -- d mod (p-1)
             exponent2         INTEGER,  -- d mod (q-1)
             coefficient       INTEGER,  -- (inverse of q) mod p
             otherPrimeInfos   OtherPrimeInfos OPTIONAL
        }
        """
        self.version: int | str = 0
        self.modulus = n
        self.publicExponent = e
        self.privateExponent = d
        self.prime1 = p
        self.prime2 = q
        self.exponent1 = d % (p-1)
        self.exponent2 = d % (q-1)
        self.coefficient = pow(q, -1, p)

    def __repr__(self) -> str:
        seq = "RSAPrivateKey ::= {\n"
        for name, value in vars(self).items():
            seq += f"\t{name}:\t{value}\n"
        seq += "}"
        return seq
        

def get_e_exponent(l_n: int):
    e = random.randint(3, l_n - 1)
    while gcd(e, l_n) != 1:
        e = random.randint(2, l_n - 1)
    return e


def generate_keys(key_len: int = 512):
    p, q = get_prime(key_len), get_prime(key_len)

    n = p * q

    l_n = lcm(p-1, q-1)

    # e = get_e_exponent(l_n)
    e = 65537
    d = pow(e, -1, l_n)

    return RSAPublicKey(n, e), RSAPrivateKey(n, e, d, p, q)

if __name__ == "__main__":
    pub, priv = generate_keys(int(input("input key len: ")))
    print(pub)
    print(priv)
