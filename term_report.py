import time
import timeit
import random
import sympy #Pip installed
from math import gcd

def generate_prime():
    primes = [i for i in range(1, 8388608) if sympy.isprime(i)]
    return random.choice(primes)


def modI(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 if x1 >= 0 else x1 + m0


def generate_keypair():
    #Get to prime numbers p and q for n = p*q
    p = generate_prime() 
    q = generate_prime()
    while p == q: #Ensure not same prime number
        q = generate_prime()

    #Compute N and N_tot
    n = p * q
    tot = (p - 1) * (q - 1)

    #Select a public key value that fufills requirement of being a multiplicative inverse
    e = random.randint(2, tot - 1)
    while gcd(e, tot) != 1:
        e = random.randint(2, tot - 1)
    d = modI(e, tot) #Generate private key
    return ((e, n), (d, n)) #Key pairs


def FindFactors(n):
    for i in range(3, n): # loops through all possible values of i between 3,..,n, missing out two because the value 2 is too insecure, therefore, not used.
        if n % i == 0: # is n (mod i) = 0, then i is a divisor of n
            return i # returns a single value for i, since there will be one and only one value since p and q are both prime.
        

def brute_force_timing():
    public_key, private_key = generate_keypair()

    #Known info to attackers
    n = public_key[1] 
    e = public_key[0]

    #N = p * q, try solve for p first
    p = FindFactors(n) # returns the prime p
    q = n//p # divide the two primes, since there is only one factor python will return the prime p
    phi_n = (p-1) * (q-1) # now we know phi(n)
    d_possible = modI(e, phi_n)
    print("Original private key:", private_key[0])
    print("Guessed private key:", d_possible)

if __name__ == "__main__":
    # Measure the time taken for the brute force operation
    time_taken = timeit.timeit(brute_force_timing, number=1)
    print("Time taken:", time_taken, "seconds")