import base64
import pathlib
import random
import string
from datetime import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from config.config import settings as app_config


def numeric_random(length: int = 16) -> str:
    """
    生成指定长度的字母和数字的随机字符串
    """
    str_list = [random.choice(string.ascii_letters + string.digits) for i in range(length)]
    return ''.join(str_list)


def format_datetime(value: datetime):
    """
    格式化成（年-月-日 时-分-秒）
    """
    if not value:
        return None
    return value.strftime('%Y-%m-%d %H:%M:%S')


def generate_public_key():
    """
    生成公钥，并保存到文件
    """
    filename = app_config.BASE_PATH + "\\key.data"
    key = rsa.generate_private_key(public_exponent=65537,
                                   key_size=4096,
                                   backend=default_backend()
                                   )
    public_key = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    if pathlib.Path(filename).exists():
        pathlib.Path(filename).unlink()

    with open(app_config.BASE_PATH + "\\key.data", 'wb') as pem_out:
        for line in public_key.splitlines():
            pem_out.write(base64.b64encode(line))


def load_key() -> str:
    """
    从文件中获取公钥
    """
    filename = app_config.BASE_PATH + "\\key.data"
    if pathlib.Path(filename).is_file():
        with open(filename, 'rb') as pem_in:
            pem_lines = pem_in.read()
        return str(pem_lines, encoding="utf-8")
    else:
        generate_public_key()
        with open(filename, 'rb') as pem_in:
            pem_lines = pem_in.read()
        return str(pem_lines, encoding="utf-8")
