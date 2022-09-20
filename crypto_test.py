from PIL import Image
import random
import string
import sys
import crypto
sys.modules['Crypto'] = crypto # 신기한거 하나 나왔읍니다
from crypto.Cipher import AES
import cv2

img_path = './Rage.png'
format = 'bmp'


def key_generator(size = 32, chars = string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def pad(data):
    return data + b"\x00" * (32 - len(data) % 32)


def trans_format_RGB(data):
    #tuple: Immutable, ensure that data is not lost
    red, green, blue = tuple(map(lambda e: [data[i] for i in range(0, len(data)) if i % 3 == e], [0, 1, 2]))
    pixels = tuple(zip(red, green, blue))
    return pixels


def aes_ecb_encrypt(key, data, mode=AES.MODE_ECB):
    aes = AES.new(key.encode('utf8'), mode)
    new_data = aes.encrypt(data)
    return new_data


def encrypt_image_ecb(filename):
    #Open the bmp picture and convert it to RGB image
    im = Image.open(filename)
    #Convert image data into pixel value bytes
    value_vector = im.convert("RGB").tobytes()

    imlength = len(value_vector)
    #for i in range(original):
        #print(data[i])
    #Map the pixel value of the filled and encrypted data
    value_encrypt = trans_format_RGB(aes_ecb_encrypt(key, pad(value_vector))[:imlength])
    #for i in range(original):
        #print(new[i])

    #Create a new object, store the corresponding value
    im2 = Image.new(im.mode, im.size)
    im2.putdata(value_encrypt)

    # Save the object as an image in the corresponding format
    im2.save('encrypted_ecb' + "." + format, format)


key = 'mtpsmimdzgvbvyppucnhotuxyijrodnh'
encrypt_image_ecb(img_path)
