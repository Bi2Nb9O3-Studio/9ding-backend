import base64
from PIL import Image
from io import BytesIO
import PIL
import PIL.Image
import watermarker
import watermarker.marker
watermarker.marker.TTF_FONT = "../font/FiraCode-Regular.ttf"
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
