import sqlite3
import numpy as np
from datetime import datetime
#from Crypto.Random import get_random_bytes
#from Crypto.Util.Padding import pad, unpad
#from Crypto.Cipher import AES


#key = get_random_bytes(16)
#iv = get_random_bytes(16)
# Ensure tables exist
def init_db():
    with sqlite3.connect("Faces.db") as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS faces_encodings(
                     encoding BLOB,name text)""")
        c.execute("""CREATE TABLE IF NOT EXISTS login_Attempts(
                     timestamp datetime,
                     status text)""")
        conn.commit()

def upload_encoding(encoding):
    with sqlite3.connect("Faces.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO faces_encodings (encoding) VALUES (?)", (encoding,))
        conn.commit()

def fetch_encoding():
    encodings = []
    with sqlite3.connect("Faces.db") as conn:
        c = conn.cursor()
        c.execute("SELECT encoding FROM faces_encodings")
        rows = c.fetchall()

        for row in rows:
            encoding_blob = row[0]
            encoding_array = np.frombuffer(encoding_blob, dtype=np.float64)
            encodings.append(encoding_array)

    return encodings  # conn auto-closes here

def LogAttempt(status):
    with sqlite3.connect("Faces.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO login_Attempts (timestamp, status) VALUES(?,?)",
                  (datetime.now(), status))
        conn.commit()
"""def encrypt_data(data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    processed_data = data.tobytes()
    padded_data = pad(processed_data, AES.block_size)
    cipher_data = cipher.encrypt(padded_data)
    return cipher_data
def decrypt_data(encrypted_data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded_data = cipher.decrypt(encrypted_data)
    decrypted_data = unpad(decrypted_padded_data, AES.block_size)  # Unpad data
    return np.frombuffer(decrypted_data, dtype=np.float64)
# Initialize database tables"""
init_db()
