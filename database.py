import sqlite3
import numpy as np
from datetime import datetime
conn = sqlite3.connect("Faces.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS faces_encodings(
encoding BLOB)""")
c.execute("""CREATE TABLE IF NOT EXISTS login_Attempts(
timestamp datetime,
status text)""")
conn.commit()
def upload_encoding(encoding):
    c.execute("INSERT INTO faces_encodings (encoding) VALUES (?)", (encoding,))
    conn.commit()
def fetch_encoding():
        """
        Loads all face encodings from the database into memory once.
        """

        c.execute("SELECT encoding FROM faces_encodings")
        rows = c.fetchall()
        encodings = []

        for row in rows:
            encoding_blob = row[0]
            encoding_array = np.frombuffer(encoding_blob, dtype=np.float64)
            encodings.append(encoding_array)

        conn.commit()
        return encodings
def LogAttempt(status):
    c.execute("""INSERT INTO login_Attempts (timestamp,status) VALUES(?,?)""",(datetime.now(),status))
    conn.commit()

