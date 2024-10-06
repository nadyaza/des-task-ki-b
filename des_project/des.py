import random 
from utils import pad, unpad, text_to_bin, bin_to_text

class DES:
    IP = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    FP = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

    E = [32, 1, 2, 3, 4, 5, 4, 5,
         6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1]

    P = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]

    def __init__(self):
        self.key = self.generate_key()
        self.iv = self.generate_iv()

    def permute(self, block, table):
        return ''.join([block[i - 1] for i in table])

    def xor(self, bits1, bits2):
        return ''.join(['0' if bits1[i] == bits2[i] else '1' for i in range(len(bits1))])

    def f(self, right, subkey):
        expanded = self.permute(right, self.E)
        xor_result = self.xor(expanded, subkey)
        return self.permute(xor_result, self.P)

    def generate_key(self):
        return ''.join([str(random.randint(0, 1)) for _ in range(64)])

    def generate_subkey(self, round_num):
        return self.key[:48]

    def generate_iv(self):
        return ''.join([str(random.randint(0, 1)) for _ in range(64)])

    def encrypt_block(self, plain_text_block):
        permuted_text = self.permute(plain_text_block, self.IP)
        left, right = permuted_text[:32], permuted_text[32:]

        for i in range(16):
            subkey = self.generate_subkey(i)
            new_right = self.xor(left, self.f(right, subkey))
            left, right = right, new_right

        return self.permute(right + left, self.FP)

    def decrypt_block(self, cipher_text_block):
        permuted_text = self.permute(cipher_text_block, self.IP)
        left, right = permuted_text[:32], permuted_text[32:]

        for i in range(15, -1, -1):
            subkey = self.generate_subkey(i)
            new_right = self.xor(left, self.f(right, subkey))
            left, right = right, new_right

        return self.permute(right + left, self.FP)

    def encrypt_cbc(self, plain_text):
        plain_text_bin = pad(text_to_bin(plain_text))
        blocks = [plain_text_bin[i:i + 64] for i in range(0, len(plain_text_bin), 64)]
        cipher_blocks = []
        prev_cipher_block = self.iv

        for block in blocks:
            xored_block = self.xor(block, prev_cipher_block)
            cipher_block = self.encrypt_block(xored_block)
            cipher_blocks.append(cipher_block)
            prev_cipher_block = cipher_block

        return ''.join(cipher_blocks)

    def decrypt_cbc(self, cipher_text):
        blocks = [cipher_text[i:i + 64] for i in range(0, len(cipher_text), 64)]
        plain_blocks = []
        prev_cipher_block = self.iv

        for block in blocks:
            decrypted_block = self.decrypt_block(block)
            plain_block = self.xor(decrypted_block, prev_cipher_block)
            plain_blocks.append(plain_block)
            prev_cipher_block = block

        return bin_to_text(unpad(''.join(plain_blocks)))
