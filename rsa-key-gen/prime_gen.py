import random

def rand(n):
    return random.randint(2**(n-1), 2**n-1)
    
def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    # Write n as (2^r)*d + 1
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
    
def get_prime(n):
    num = rand(n)
    while not is_prime(num):
        num += 1
    return num

if __name__ == "__main__":
    print(get_prime(int(input("Input len of prime num in bits: "))))
    
    
