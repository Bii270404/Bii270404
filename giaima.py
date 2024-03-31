import tkinter as tk
import re

def generate_playfair_matrix(key):
    # Xây dựng ma trận Playfair từ khóa
    key = re.sub(r'[^a-zA-Z]', '', key.upper())
    key = ''.join(dict.fromkeys(key))  # Loại bỏ các ký tự trùng lặp
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Bỏ qua 'J' theo quy ước
    matrix = []

    # Tạo ma trận 5x5 từ khóa
    for char in key:
        if char not in matrix and char in alphabet:
            matrix.append(char)

    for char in alphabet:
        if char not in matrix:
            matrix.append(char)

    # Chia ma trận thành các hàng con
    matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    return matrix

def encode(plaintext, key):
    matrix = generate_playfair_matrix(key)
    plaintext = re.sub(r'[^a-zA-Z]', '', plaintext.upper())
    ciphertext = ""
    pairs = re.findall(r'(?:(.)(?!\1)(.))', plaintext)  # Chia thành các cặp ký tự khác nhau

    for pair in pairs:
        row1, col1 = divmod(matrix.index([char for char in pair[0] if char in matrix][0]), 5)
        row2, col2 = divmod(matrix.index([char for char in pair[1] if char in matrix][0]), 5)

        if row1 == row2:  # Cùng hàng
            ciphertext += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:  # Cùng cột
            ciphertext += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:  # Khác hàng và cột
            ciphertext += matrix[row1][col2] + matrix[row2][col1]

    return ciphertext

def decode(ciphertext, key):
    matrix = generate_playfair_matrix(key)
    plaintext = ""
    pairs = re.findall(r'(?:(.)(?!\1)(.))', ciphertext.upper())

    for pair in pairs:
        row1, col1 = divmod(matrix.index([char for char in pair[0] if char in matrix][0]), 5)
        row2, col2 = divmod(matrix.index([char for char in pair[1] if char in matrix][0]), 5)

        if row1 == row2:  # Cùng hàng
            plaintext += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:  # Cùng cột
            plaintext += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:  # Khác hàng và cột
            plaintext += matrix[row1][col2] + matrix[row2][col1]

    return plaintext

def encode_playfair(plaintext, key):
    return encode(plaintext, key)

def decode_playfair(ciphertext, key):
    return decode(ciphertext, key)

def main():
    root = tk.Tk()
    root.title("Ứng dụng mã Playfair")

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Thông điệp:").grid(row=0, column=0)
    plaintext_entry = tk.Entry(input_frame)
    plaintext_entry.grid(row=0, column=1)

    tk.Label(input_frame, text="Khóa:").grid(row=1, column=0)
    key_entry = tk.Entry(input_frame)
    key_entry.grid(row=1, column=1)

    encode_button = tk.Button(root, text="Mã hóa", command=lambda: encode())
    encode_button.pack(pady=5)

    decode_button = tk.Button(root, text="Giải mã", command=lambda: decode())
    decode_button.pack(pady=5)

    result_label = tk.Label(root, text="")
    result_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
