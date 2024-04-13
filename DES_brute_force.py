from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
import time
import matplotlib.pyplot as plt
import numpy as np

#function to generate a DES key where only first n-bits can be changed
def generate_partial_des_key(n_bits, key_candidate):
    candidate_bytes = key_candidate.to_bytes((n_bits + 7) // 8, 'big')
    #ensure key is exactly 8 bytes long, padding with zeros if necessary
    return (candidate_bytes + b'\x00' * 8)[:8]

#brute force function to find the key for the first n-bits
def brute_force_des(ciphertext, known_plaintext, n_bits):
    start_time = time.time()
    #key space size = 2^n_bits
    key_space_size = 1 << n_bits
    #generates every possible key candidate in the space of the key size until it finds match
    for key_candidate in range(key_space_size):
        key = generate_partial_des_key(n_bits, key_candidate)
        cipher = DES.new(key, DES.MODE_ECB)
        try:
            decrypted_text = unpad(cipher.decrypt(ciphertext), DES.block_size).decode('utf-8')
            if known_plaintext in decrypted_text:
                end_time = time.time()
                return key_candidate, decrypted_text, end_time - start_time
        except ValueError:
            continue
    return None

#define plaintext message
plaintext = "This is my plaintext message."
plaintext_bytes = pad(plaintext.encode('utf-8'), DES.block_size)

#number of trials
trials = 10

#key lengths to test
key_range = range(1, 25)  #1 to 24 bits, also used 1 to 16 to show more specific times for lower bit ranges

#dictionary to store execution times
times = {k: [] for k in key_range}

#running brute-force multiple times
for n_bits in key_range:
    for _ in range(trials):
        #generating random key
        random_bits = get_random_bytes((n_bits + 7) // 8)
        random_key_part = int.from_bytes(random_bits, 'big') & ((1 << n_bits) - 1)
        full_key = generate_partial_des_key(n_bits, random_key_part)
        cipher = DES.new(full_key, DES.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext_bytes)

        #brute force key
        result = brute_force_des(ciphertext, plaintext, n_bits)
        if result:
            _, _, execution_time = result
            times[n_bits].append(execution_time)
        #no solution found, should never occur
        else:
            times[n_bits].append(float('inf'))

#calculates average times for each key length
avg_times = [np.mean(times[k]) for k in key_range]

#plot results
plt.plot(list(key_range), avg_times, marker='o')
plt.title('Average Execution Time vs Key Length')
plt.xlabel('Key Length (bits)')
plt.ylabel('Execution Time (seconds)')
plt.grid(True)
plt.show()
