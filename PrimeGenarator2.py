import random
from math import gcd, sqrt
import time

def factorize(N):
    for i in range(2, int(sqrt(N)) + 1):
        if N % i == 0:
            p = i
            q = N // i
            return p, q
    return None, None

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def generate_prime(min_val, max_val):
    while True:
        num = random.randint(min_val, max_val)
        if is_prime(num):
            return num
        
def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def calculate_private_exponent(e, phi):
    d = modinv(e, phi)
    return d

def generate_test_case(bit_size):
    min_val = 2**(bit_size - 1)
    max_val = 2**bit_size - 1

    p = generate_prime(min_val, max_val)
    q = generate_prime(min_val, max_val)
    N = p * q
    phi = (p - 1) * (q - 1)
    e = random.choice([3, 5, 17, 257, 65537])
    while gcd(e, phi) != 1:
        e = random.choice([3, 5, 17, 257, 65537])
    
    d = calculate_private_exponent(e, phi)
    
    return p, q, N, e, d

def encrypt(message, e, N):
    encrypted_message = [pow(ord(char), e, N) for char in message]
    return encrypted_message

def decrypt(encrypted_message, d, N):
    decrypted_message = ''.join([chr(pow(char, d, N)) for char in encrypted_message])
    return decrypted_message

def test_rsa_and_factorization(bit_size):
    print(f"Testing {bit_size}-bit RSA key:")
    
    
    p, q, N, e, d = generate_test_case(bit_size)
    
    print(f"Generated RSA Modulus (N): {N}")
    
   
    start_time = time.perf_counter()
    found_p, found_q = factorize(N)
    end_time = time.perf_counter()
    
    if found_p is not None and found_q is not None:
        print(f"Factored N into p = {found_p}, q = {found_q}")
    else:
        print("Failed to factorize N.")
    
    runtime = end_time - start_time
    print(f"Public exponent (e): {e}, Private exponent (d): {d}")
    print(f"Runtime: {runtime:.6f} seconds\n")
    
   
    test_message = "Hi"
    encrypted_message = encrypt(test_message, e, N)
    decrypted_message = decrypt(encrypted_message, d, N)
    print(f"Original Message: {test_message}")
    print(f"Encrypted Message: {encrypted_message}")
    print(f"Decrypted Message: {decrypted_message}\n")


test_rsa_and_factorization(8)


test_rsa_and_factorization(16)
