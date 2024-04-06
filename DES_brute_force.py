from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes


# 1. Define a plaintext message
plaintext = "Hello, DES!"

# 2. Convert plaintext to bytes and pad it
plaintext_bytes = pad(plaintext.encode('utf-8'), DES.block_size)

# 3. Generate a random 8-bit value for small_key
small_key = get_random_bytes(1)[0]


# Adjusting the function to properly generate a 64-bit DES key from an 8-bit base key
def generate_des_key_from_small_key(small_key):
    # Expand the small key to fill 56 bits and add an empty byte for parity, forming a 64-bit key
    expanded_key = (small_key.to_bytes(1, 'big') * 7) + b'\x00'
    return expanded_key

# Updated brute force function using the corrected key generation logic
def brute_force_des(ciphertext, known_plaintext):
    for key_candidate in range(256):  # All possible values for an 8-bit key
        # Generate a DES key from the 8-bit candidate
        key = generate_des_key_from_small_key(key_candidate)
        cipher = DES.new(key, DES.MODE_ECB)
        try:
            decrypted_text = unpad(cipher.decrypt(ciphertext), DES.block_size).decode('utf-8')
            if known_plaintext in decrypted_text:
                return key_candidate, decrypted_text
        except ValueError:
            # Handle padding errors
            continue
    return None, None

# Encrypt the plaintext again with the adjusted key generation
des_key = generate_des_key_from_small_key(small_key)  # Generate a valid DES key from the 8-bit base

# Encrypt the plaintext
cipher = DES.new(des_key, DES.MODE_ECB)
ciphertext = cipher.encrypt(plaintext_bytes)

# Attempt to brute force the key
found_key_candidate, decrypted_message = brute_force_des(ciphertext, plaintext)

#small_key, found_key_candidate, decrypted_message
