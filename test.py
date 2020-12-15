from Crypto.Cipher import DES


def lcm(a, b):
    m = a * b
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return m // (a + b)


key = b"qwertyui"
msg = b"hello world!"

if len(msg) % 16 != 0:
    space_num = lcm(len(msg), 16)
    msg = msg + b" " * space_num

obj = DES.new(key, DES.MODE_ECB)
print(len(msg))

e_msg = obj.encrypt(msg)
print(obj.decrypt(e_msg))
