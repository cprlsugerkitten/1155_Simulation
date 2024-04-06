from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Define the block size for DES
block_size = DES.block_size

# Generate a random DES key
key = get_random_bytes(block_size)

# Fixed IV for OFB mode
IV_fixed = get_random_bytes(block_size)

# Known plaintext and corresponding ciphertext (the attacker has somehow obtained these)
known_plaintext = pad(b'KnownMessage', block_size)
cipher_ofb = DES.new(key, DES.MODE_OFB, IV_fixed)
known_ciphertext = cipher_ofb.encrypt(known_plaintext)

# Attacker derives the keystream used for the known plaintext
def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

# XOR the known plaintext with the known ciphertext to get the keystream
keystream = xor_bytes(known_plaintext, known_ciphertext)

# Now, if the attacker intercepts a new ciphertext encrypted with the same key and IV, they can decrypt it
new_ciphertext = cipher_ofb.encrypt(pad(b'NewSecretMsg', block_size))  # This would be captured by the attacker
decrypted_new_plaintext = xor_bytes(new_ciphertext, keystream)

print("Known Plaintext:", known_plaintext)
print("Known Ciphertext:", known_ciphertext)
print("Keystream Derived by Attacker:", keystream)
print("Intercepted New Ciphertext:", new_ciphertext)
print("Decrypted New Plaintext:", decrypted_new_plaintext)
