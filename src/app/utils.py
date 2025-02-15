from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import AES
import base64
from PIL import Image
from io import BytesIO
import PIL
import PIL.Image
import watermarker
import watermarker.marker
watermarker.marker.TTF_FONT = "./FiraCode-Regular.ttf"
def baseN(num, b):
    '''进制PlusProMax'''
    return ((num == 0) and "0") or (baseN(num // b, b).lstrip("0") + r"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ;:/\|<>@#$%&-+"[num % b])


def ch3(x):
    '''ipv4转数字IP'''
    return sum([256**j*int(i)
                        for j, i in enumerate(x.split('.')[::-1])])


def imgopen(base64_string):
    head, context = base64_string.split(",")  # 将base64_str以“,”分割为两部分
    img_data = base64.b64decode(context)    # 解码时只要内容部分

    image = Image.open(BytesIO(img_data))
    return image


def watermarktxt(request, id: int):
    str = ""
    str += baseN(ch3(request.remote_addr),76)
    str += "="
    str += baseN(id, 50)
    return str


def watermarkimg(img, txt) -> PIL.Image.Image:
    return watermarker.marker.im_add_mark(img, txt, size=20,space=10)


# encrypt

"""
ECB没有偏移量
"""
key ='WnjdH1xTxVBpHMezzIRhPEbbxmxtIYvr'.encode('utf-8')

def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# 加密函数
def encrypt(text):
    mode = AES.MODE_ECB
    text = add_to_16(text)
    cryptos = AES.new(key, mode)

    cipher_text = cryptos.encrypt(text)
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text):
    mode = AES.MODE_ECB
    cryptor = AES.new(key, mode)
    plain_text = cryptor.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')