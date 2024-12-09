# app/gq_protocol.py
import hashlib
import os

# Parámetros públicos del protocolo GQ
# Para propósitos de demostración, utilizamos valores pequeños.
N = 162259276829213363391578010288127  # Un número primo grande
G = 5  # Generador

def hash_password(password):
    """
    Hash de la contraseña usando SHA-256 para derivar el secreto x.
    """
    return int(hashlib.sha256(password.encode()).hexdigest(), 16)

def compute_public_key(x):
    """
    Computa la clave pública y = g^x mod n.
    """
    return pow(G, x, N)

def compute_proof(r, c, x):
    """
    Computa la prueba s = r + c * x mod (n-1).
    """
    return (r + c * x) % (N - 1)

def verify_proof(u, s, y, c):
    """
    Verifica si g^s mod n == u * y^c mod n.
    """
    lhs = pow(G, s, N)
    rhs = (u * pow(y, c, N)) % N
    return lhs == rhs
