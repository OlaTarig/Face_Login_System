from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import face_recognition
key = get_random_bytes(16)
iv = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
data = face_recognition.face_encodings("Elon2.png")
processed_data = data.tobytes()
padded_data = pad(data, AES.block_size)
cipher_data = cipher.encrypt(padded_data)
cipher_dec = AES.new(key, AES.MODE_CBC, iv)
decrypted_padded_data = cipher_dec.decrypt(ciphertext)
decrypted_data = unpad(decrypted_padded_data, AES.block_size)
print(f"Ciphertext: {ciphertext}")
print(f"Decrypted Data: {decrypted_data.decode('utf-8')}")
