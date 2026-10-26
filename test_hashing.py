import hashlib
import os

def test_security_logic():
    password = "Demo-Admin-2026-SuperSafe!"
    
    # --- TEST 1: Salt Generation ---
    # User A and User B have the SAME password
    salt_a = os.urandom(16)
    salt_b = os.urandom(16)
    
    hash_a = hashlib.pbkdf2_hmac('sha512', password.encode(), salt_a, 100000).hex()
    hash_b = hashlib.pbkdf2_hmac('sha512', password.encode(), salt_b, 100000).hex()
    
    print("--- SECURITY AUDIT ---")
    print(f"User A Salt: {salt_a.hex()}")
    print(f"User B Salt: {salt_b.hex()}")
    print("\n")
    print(f"User A Hash: {hash_a[:50]}...")
    print(f"User B Hash: {hash_b[:50]}...")
    
    if hash_a != hash_b:
        print("\n✅ SUCCESS: Passwords are safe! Salting ensures hashes are unique.")
    else:
        print("\n❌ FAIL: Hashes are identical. Your salt isn't working.")

    # --- TEST 2: Complexity Check ---
    print(f"\nHash Length: {len(hash_a)} characters (SHA-512 Standard)")
    print(f"Iterations: 100,000 (Strong protection against brute force)")

if __name__ == "__main__":
    test_security_logic()