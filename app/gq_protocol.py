import hashlib
import os

# Parámetros públicos del protocolo GQ (N, G)
N = 162259276829213363391578010288127
G = 5

def hash_password(password):
    """
    Hash de la contraseña usando SHA-256 para derivar el secreto w.
    password.strip() para evitar espacios o saltos de línea extra.
    """
    password = password.strip()
    return int(hashlib.sha256(password.encode()).hexdigest(), 16)

def compute_public_key(w):
    """
    y = g^w mod N
    """
    return pow(G, w, N)

def compute_commitment():
    """
    Genera t aleatorio y u = g^t mod N
    """
    t = int.from_bytes(os.urandom(16), 'big') % N
    u = pow(G, t, N)
    return t, u

def verify_proof(u, s, y, c):
    """
    Verifica si g^s mod N == u * y^c mod N.
    Con s = t + c*w se cumple:
    g^(t+c*w) = g^t * g^(c*w) = u * (g^w)^c = u * y^c mod N
    """
    lhs = pow(G, s, N)
    rhs = (u * pow(y, c, N)) % N
    return lhs == rhs
