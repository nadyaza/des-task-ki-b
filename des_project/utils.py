def pad(text):
    padding_len = (64 - (len(text) % 64)) % 64
    return text + '0' * padding_len

def unpad(text):
    return text.rstrip('0')

def text_to_bin(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_text(binary):
    chars = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)
