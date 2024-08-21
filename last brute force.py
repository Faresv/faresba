import math
import time
import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    gcd, x, y = gcd_extended(e, phi)
    if gcd != 1:
        return None  # Modular inverse does not exist
    else:
        return x % phi

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_random_prime(bits):
    while True:
        prime_candidate = random.getrandbits(bits)
        prime_candidate |= (1 << bits - 1) | 1  # Ensure it is odd and has the right bit length
        if is_prime(prime_candidate):
            return prime_candidate

def factorize(N):
    # Simple trial division up to sqrt(N)
    for i in range(2, int(math.sqrt(N)) + 1):
        if N % i == 0:
            return i, N // i
    return None, None  # If no factors are found (N is prime or factorization failed)

def calculate_phi_n(N):
    p, q = factorize(N)
    if p is None or q is None:
        return None  # Factorization failed
    return (p - 1) * (q - 1)

def brute_force_private_exponent(e, N):
    phi_n = calculate_phi_n(N)
    if phi_n is None:
        return None  # Failed to calculate phi_n

    for d in range(1, phi_n):
        if (d * e) % phi_n == 1:
            return d
    return None  # If no valid d is found within the range

def generate_test_cases(bits):
    while True:
        p = generate_random_prime(bits)
        q = generate_random_prime(bits)
        if p != q:
            break
    N = p * q
    e = 65537  # Common public exponent
    return N, e

def encrypt(message, e, N):
    encrypted_message = [pow(ord(char), e, N) for char in message]
    return encrypted_message

def decrypt(encrypted_message, d, N):
    decrypted_message = ''.join([chr(pow(char, d, N)) for char in encrypted_message])
    return decrypted_message

def main():
    test_cases = [8, 16]
    runtimes = []

    for bits in test_cases:
        for _ in range(2):  # Generate two test cases for each bit size
            N, e = generate_test_cases(bits)
            print(f"Testing with {bits}-bit values:")
            print(f"N: {N}, e: {e}")
            
            start_time = time.perf_counter()
            d = brute_force_private_exponent(e, N)
            end_time = time.perf_counter()
            
            if d is not None:
                print(f"Private exponent d: {d}")
                
                # Validate by encryption and decryption
                test_message = "Hi"
                encrypted_message = encrypt(test_message, e, N)
                decrypted_message = decrypt(encrypted_message, d, N)
                
                print(f"Original Message: {test_message}")
                print(f"Encrypted Message: {encrypted_message}")
                print(f"Decrypted Message: {decrypted_message}")
                
                if test_message == decrypted_message:
                    print("Validation successful: Decrypted message matches the original message.")
                else:
                    print("Validation failed: Decrypted message does not match the original message.")
                    
            else:
                print("Failed to calculate the private exponent.")
            
            runtime = end_time - start_time
            print(f"Runtime: {runtime:.6f} seconds\n")
            runtimes.append((N, runtime))
    
    # Report runtimes for different values of N
    for N, runtime in runtimes:
        print(f"N: {N}, Runtime: {runtime:.6f} seconds")

if __name__ == "__main__":
    main()
