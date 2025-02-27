import sqlite3
import numpy as np
from datetime import datetime

# Ensure tables exist
def init_db():
    with sqlite3.connect("Faces.db") as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS faces_encodings(
                     encoding BLOB)""")
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
    """
    Loads all face encodings from the database into memory once.
    """
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

# Initialize database tables
init_db()
