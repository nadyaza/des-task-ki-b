from des import DES

def main():
    des = DES()
    print(f"Generated Key: {des.key}")
    print(f"Generated IV: {des.iv}")

    plain_text = input("Masukkan teks yang ingin dienkripsi: ")
    print(f"Plain Text: {plain_text}")

    cipher_text = des.encrypt_cbc(plain_text)
    print(f"Cipher Text: {cipher_text}")

    decrypted_text = des.decrypt_cbc(cipher_text)
    print(f"Decrypted Text: {decrypted_text}")

if __name__ == "__main__":
    main()
