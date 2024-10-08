import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import numpy as np

# Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    key = key.lower()
    key_length = len(key)
    key_as_int = [ord(i) - 97 for i in key]
    plaintext_int = [ord(i) - 97 for i in plaintext.lower() if i.isalpha()]
    ciphertext = ''
    
    for i in range(len(plaintext_int)):
        value = (plaintext_int[i] + key_as_int[i % key_length]) % 26
        ciphertext += chr(value + 97)
        
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    key = key.lower()
    key_length = len(key)
    key_as_int = [ord(i) - 97 for i in key]
    ciphertext_int = [ord(i) - 97 for i in ciphertext.lower()]
    plaintext = ''
    
    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
        plaintext += chr(value + 97)
        
    return plaintext

# Playfair Cipher
def generate_playfair_table(key):
    key = "".join(dict.fromkeys(key.lower().replace("j", "i"))) 
    alphabet = "abcdefghiklmnopqrstuvwxyz"
    table = []
    
    for char in key + alphabet:
        if char not in table:
            table.append(char)
            
    matrix = [table[i:i+5] for i in range(0, 25, 5)]
    return matrix

def playfair_encrypt(plaintext, key):
    matrix = generate_playfair_table(key)
    plaintext = plaintext.replace("j", "i").lower()
    if len(plaintext) % 2 != 0:
        plaintext += 'x'
    
    def get_position(char):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == char:
                    return row, col

    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        row1, col1 = get_position(plaintext[i])
        row2, col2 = get_position(plaintext[i + 1])

        if row1 == row2:
            ciphertext += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += matrix[row1][col2] + matrix[row2][col1]

    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = generate_playfair_table(key)
    
    def get_position(char):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == char:
                    return row, col

    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        row1, col1 = get_position(ciphertext[i])
        row2, col2 = get_position(ciphertext[i + 1])

        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += matrix[row1][col2] + matrix[row2][col1]

    return plaintext

# Hill Cipher
def hill_encrypt(plaintext, key_matrix):
    n = len(key_matrix)
    plaintext = [ord(char) - ord('a') for char in plaintext.lower() if char.isalpha()]
    while len(plaintext) % n != 0:
        plaintext.append(ord('x') - ord('a'))

    ciphertext = []
    for i in range(0, len(plaintext), n):
        block = np.dot(key_matrix, plaintext[i:i+n]) % 26
        ciphertext.extend(block)
    
    return ''.join([chr(c + ord('a')) for c in ciphertext])

def hill_decrypt(ciphertext, key_matrix):
    n = len(key_matrix)
    ciphertext = [ord(char) - ord('a') for char in ciphertext.lower()]
    
    key_inverse = np.linalg.inv(key_matrix).astype(int) % 26

    plaintext = []
    for i in range(0, len(ciphertext), n):
        block = np.dot(key_inverse, ciphertext[i:i+n]) % 26
        plaintext.extend(block)
    
    return ''.join([chr(p + ord('a')) for p in plaintext])

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            message_entry.delete(0, tk.END)
            message_entry.insert(0, file.read())

def save_file(text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text)

def encrypt():
    cipher = cipher_var.get()
    key = key_entry.get()
    text = message_entry.get()

    if len(key) < 12:
        messagebox.showerror("Error", "Kunci minimal harus 12 karakter.")
        return

    if cipher == "Vigenere":
        result = vigenere_encrypt(text, key)
    elif cipher == "Playfair":
        result = playfair_encrypt(text, key)
    elif cipher == "Hill":
        key_matrix = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
        result = hill_encrypt(text, key_matrix)

    encrypted_text.delete(1.0, tk.END) 
    encrypted_text.insert(tk.END, result)

def decrypt():
    cipher = cipher_var.get()
    key = key_entry.get()
    text = message_entry.get()

    if len(key) < 12:
        messagebox.showerror("Error", "Kunci minimal harus 12 karakter.")
        return

    if cipher == "Vigenere":
        result = vigenere_decrypt(text, key)
    elif cipher == "Playfair":
        result = playfair_decrypt(text, key)
    elif cipher == "Hill":
        key_matrix = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
        result = hill_decrypt(text, key_matrix)

    decrypted_text.delete(1.0, tk.END)
    decrypted_text.insert(tk.END, result)

root = tk.Tk()
root.title("Program Cipher Raven")
root.geometry("600x600")
root.configure(bg='#FFC0CB')

cipher_var = tk.StringVar(value="Vigenere")
cipher_label = tk.Label(root, text="Pilih Cipher:", bg='#FFC0CB', font=("Arial", 12))
cipher_label.pack(pady=10)

cipher_frame = tk.Frame(root, bg='#FFC0CB')
cipher_frame.pack(pady=5)

for cipher in ["Vigenere", "Playfair", "Hill"]:
    cipher_button = tk.Radiobutton(cipher_frame, text=cipher, variable=cipher_var, value=cipher, bg='#FFC0CB')
    cipher_button.pack(side=tk.LEFT)
    
key_label = tk.Label(root, text="Kunci (min 12 karakter):", bg='#FFC0CB', font=("Arial", 12))
key_label.pack(pady=10)
key_entry = tk.Entry(root, width=50)
key_entry.pack(pady=5)

message_label = tk.Label(root, text="Pesan:", bg='#FFC0CB', font=("Arial", 12))
message_label.pack(pady=10)
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=5)

load_button = tk.Button(root, text="Pilih File", command=load_file, bg='#DDA0DD', fg='black')
load_button.pack(pady=5)

button_frame = tk.Frame(root, bg='#FFC0CB')
button_frame.pack(pady=10)

encrypt_button = tk.Button(button_frame, text="Enkripsi", command=encrypt, bg='#DDA0DD', fg='black')
encrypt_button.pack(side=tk.LEFT, padx=5)

decrypt_button = tk.Button(button_frame, text="Dekripsi", command=decrypt, bg='#DDA0DD', fg='black')
decrypt_button.pack(side=tk.LEFT, padx=5)

result_frame = tk.Frame(root, bg='#FFC0CB')
result_frame.pack(pady=10)

encrypted_label = tk.Label(result_frame, text="Hasil Enkripsi:", bg='#FFC0CB', font=("Arial", 12))
encrypted_label.pack(anchor='w')
encrypted_text = scrolledtext.ScrolledText(result_frame, width=50, height=5, bg='#FFFFFF', font=("Arial", 12))  # Pink tua
encrypted_text.pack()

decrypted_label = tk.Label(result_frame, text="Hasil Dekripsi:", bg='#FFC0CB', font=("Arial", 12))
decrypted_label.pack(anchor='w')
decrypted_text = scrolledtext.ScrolledText(result_frame, width=50, height=5, bg='#FFFFFF', font=("Arial", 12))  # Pink tua
decrypted_text.pack()

root.mainloop()