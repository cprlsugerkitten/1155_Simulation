from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Define the block size for DES
block_size = DES.block_size

# Generate a random DES key
key = get_random_bytes(block_size)

# Known IV used for Bob's encryption
IV_bob = get_random_bytes(block_size)

# Eve's predictable IV for the next message
IV_eve = IV_bob

# Encrypt Bob's vote (let's say he voted for P1)
P1 = b'P1'
P2 = b'P2'
bob_vote = pad(P1, block_size)  # Assuming P1 is the chosen vote and is a single block

# Eve's chosen plaintext for her attack
eve_chosen_plaintext = pad(b'Eve_Attack', block_size)

# Bob's vote encrypted with IV_bob
cipher_bob = DES.new(key, DES.MODE_CBC, IV_bob)
ciphertext_bob = cipher_bob.encrypt(bob_vote)

# Eve's chosen plaintext encrypted with IV_eve (which she knows/predicts)
cipher_eve = DES.new(key, DES.MODE_CBC, IV_eve)
ciphertext_eve = cipher_eve.encrypt(eve_chosen_plaintext)

# Function to perform XOR between two strings of bytes
def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

# If Eve's plaintext was chosen such that it's the same as Bob's vote but with flipped bits
# Eve can derive Bob's plaintext by xoring the ciphertexts (since IVs are the same, they cancel out)
eve_derived_plaintext = xor_bytes(ciphertext_bob, ciphertext_eve)

print("Bob's Original Vote:", bob_vote)
print("Bob's Encrypted Vote:", ciphertext_bob)
print("Eve's Chosen Plaintext:", eve_chosen_plaintext)
print("Eve's Encrypted Plaintext:", ciphertext_eve)
print("Eve Derived Bob's Plaintext:", eve_derived_plaintext)
