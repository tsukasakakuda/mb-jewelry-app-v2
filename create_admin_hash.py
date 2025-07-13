#!/usr/bin/env python3
import bcrypt

password = 'admin123'
hash_value = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(f"Password: {password}")
print(f"Hash: {hash_value.decode('utf-8')}")
print()
print("Cloud SQL Studio用SQL:")
print(f"INSERT INTO users (username, password_hash, role) VALUES ('admin', '{hash_value.decode('utf-8')}', 'admin');")