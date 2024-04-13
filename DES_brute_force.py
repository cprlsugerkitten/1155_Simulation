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
    key_space_size = 1 << n_bits  # Equivalent to 2**n_bits
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

# Define plaintext message
plaintext = "Hello, DES!"
plaintext_bytes = pad(plaintext.encode('utf-8'), DES.block_size)

# Number of trials for averaging
trials = 10

#key lengths to test
key_range = range(1, 25)  # Key lengths from 1 bit to 24 bits

# Initialize dictionary to store execution times for each key length
times = {k: [] for k in key_range}

# Run the encryption and brute-force multiple times for averaging
for n_bits in key_range:
    for _ in range(trials):
        # Generate a random key part and encrypt the plaintext
        random_bits = get_random_bytes((n_bits + 7) // 8)
        random_key_part = int.from_bytes(random_bits, 'big') & ((1 << n_bits) - 1)
        full_des_key = generate_partial_des_key(n_bits, random_key_part)
        cipher = DES.new(full_des_key, DES.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext_bytes)

        # Attempt to brute force the key and measure execution time
        result = brute_force_des(ciphertext, plaintext, n_bits)
        if result:
            _, _, execution_time = result
            times[n_bits].append(execution_time)
        else:
            times[n_bits].append(float('inf'))  # Using infinity to denote no solution found

# Calculate average times for each key length
avg_times = [np.mean(times[k]) for k in key_range]

# Plotting the results
plt.plot(list(key_range), avg_times, marker='o')
plt.title('Average Execution Time vs Key Length')
plt.xlabel('Key Length (bits)')
plt.ylabel('Execution Time (seconds)')
plt.grid(True)
plt.show()
