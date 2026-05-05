import math
from collections import Counter
import hashlib
import os

def calculate_entropy(text):
    if not text:
        return 0
    
   
    counts = Counter(text)
    total_len = len(text)
    
 
    entropy = 0
    for count in counts.values():
        
        p = count / total_len
        
        entropy -= p * math.log2(p)
        
    return entropy


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    else:
        salt = bytes.fromhex(salt)
    
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return salt.hex(), hashed_password.hex()

def verify_password(stored_salt, stored_password, provided_password):
    salt, hashed_password = hash_password(provided_password, stored_salt)
    return hashed_password == stored_password


test_key = "AIzaSyB7_4fGk9z2W1m8p0Q5rX6tV3nL9sJ" 
test_word = "password123"                     

# Define a list of Normal Code strings (boilerplate code)
NORMAL_CODE_SNIPPETS = [
    "import os",
    "def main():",
    "if __name__ == '__main__':",
    "try:",
    "except Exception as e:",
    "for i in range(10):",
    "print('Hello, world!')",
    "return True",
    "class MyClass:",
    "    pass"
]

# Calculate the average entropy for the normal code snippets (Baseline)
normal_entropies = [calculate_entropy(snippet) for snippet in NORMAL_CODE_SNIPPETS]
AVERAGE_BASELINE_ENTROPY = sum(normal_entropies) / len(normal_entropies)

print(f"Average Baseline Entropy (Normal Code): {AVERAGE_BASELINE_ENTROPY:.2f}")

def generate_entropy_histogram_data(code_snippet):
    entropy_values = []
    lines = code_snippet.splitlines()
    for line in lines:
        if line.strip():
            entropy_values.append(calculate_entropy(line))
        else:
            entropy_values.append(0)
    return entropy_values





print(f"Key Entropy: {calculate_entropy(test_key):.2f}") 
print(f"Word Entropy: {calculate_entropy(test_word):.2f}")

# Example usage for histogram data generation
example_code = """
import math

def calculate_entropy(text):
    if not text:
        return 0
"""
histogram_data = generate_entropy_histogram_data(example_code)
print(f"Histogram Data for Example Code: {histogram_data}")


# Example usage of password hashing
password = "mysecretpassword"
salt, hashed_password = hash_password(password)
print(f"Salt: {salt}")
print(f"Hashed Password: {hashed_password}")

# Verify the password
is_valid = verify_password(salt, hashed_password, password)
print(f"Password is valid: {is_valid}")

is_invalid = verify_password(salt, hashed_password, "wrongpassword")
print(f"Wrong password is valid: {is_invalid}")
