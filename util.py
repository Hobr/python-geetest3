import json
import random
from binascii import hexlify
from hashlib import md5

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from loguru import logger


class GeetestBase:
    # 自定义Base64字符集, 使用标准Base64的变体（包含()代替+/）
    CUSTOM_BASE64_ALPHABET = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()"
    )

    # 预定义每个6位段对应的位位置（从高位到低位）
    # 掩码转换为对应的位位置列表, 用于直接提取所需的6位
    _PART1_BITS = [22, 21, 19, 18, 17, 16]  # 掩码7274496 (0x6F0000)
    _PART2_BITS = [23, 20, 15, 13, 12, 10]  # 掩码9483264 (0x90B400)
    _PART3_BITS = [14, 11, 9, 8, 4, 2]  # 掩码19220 (0x4B14)
    _PART4_BITS = [7, 6, 5, 3, 1, 0]  # 掩码235 (0xEB)

    def _get_base64_char(self, index: int) -> str:
        """返回自定义Base64字符集中对应索引的字符, 索引无效时返回'.'"""
        return (
            self.CUSTOM_BASE64_ALPHABET[index]
            if 0 <= index < len(self.CUSTOM_BASE64_ALPHABET)
            else "."
        )

    @staticmethod
    def _extract_bits(value: int, bits: list) -> int:
        """从给定值中按bits列表顺序提取指定位, 组合成新的6位整数"""
        result = 0
        for bit in bits:
            result = (result << 1) | ((value >> bit) & 1)
        return result

    def _encode_chunk(self, data: bytes) -> dict:
        """将字节数据分块编码, 返回结果和填充后缀"""
        encoded = []
        padding = ""
        for i in range(0, len(data), 3):
            chunk = data[i : i + 3]
            # 处理完整的3字节块
            if len(chunk) == 3:
                c = (chunk[0] << 16) | (chunk[1] << 8) | chunk[2]
                encoded.append(
                    self._get_base64_char(self._extract_bits(c, self._PART1_BITS))
                )
                encoded.append(
                    self._get_base64_char(self._extract_bits(c, self._PART2_BITS))
                )
                encoded.append(
                    self._get_base64_char(self._extract_bits(c, self._PART3_BITS))
                )
                encoded.append(
                    self._get_base64_char(self._extract_bits(c, self._PART4_BITS))
                )
            else:  # 处理余数
                remainder = len(chunk)
                c = chunk[0] << 16
                if remainder == 2:
                    c |= chunk[1] << 8
                # 提取前两部分
                encoded.append(
                    self._get_base64_char(self._extract_bits(c, self._PART1_BITS))
                )
                encoded.append(
                    self._get_base64_char(self._extract_bits(c, self._PART2_BITS))
                )
                # 根据余数处理第三部分和填充
                if remainder == 2:
                    encoded.append(
                        self._get_base64_char(self._extract_bits(c, self._PART3_BITS))
                    )
                    padding = "."
                else:
                    padding = ".."
        return {"res": "".join(encoded), "end": padding}

    def enc(self, data: bytes) -> str:
        """加密入口：将字节数据编码为自定义Base64字符串"""
        result = self._encode_chunk(data)
        return result["res"] + result["end"]


class W:
    @logger.catch
    def __init__(self, key: str, gt: str, challenge: str, c: str, s: str) -> None:
        self.key = key
        self.gt = gt
        self.challenge = challenge
        self.c = c
        self.s = s
        self.aeskey = self.Key()

    @logger.catch
    def Key(self) -> bytes:
        var = []
        for _ in range(4):
            randomValue = int(65536 * (1 + random.random()))
            hex = format(randomValue, "04x")[1:]
            var.append(hex)
        dist = ("".join(var)).encode()
        return dist

    @logger.catch
    def RSA(self, data: str) -> str:
        k = int(
            "00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81",
            16,
        )
        e = int("010001", 16)
        pubKey = RSA.construct((k, e))
        cipher = PKCS1_v1_5.new(pubKey)
        encryptedData = cipher.encrypt(data.encode())
        encryptedHex = hexlify(encryptedData)
        return encryptedHex.decode()

    @logger.catch
    def AES(self, data: str) -> list:
        iv = b"0000000000000000"
        cipher = AES.new(self.aeskey, AES.MODE_CBC, iv)
        padPkcs7 = pad(data.encode(), AES.block_size, style="pkcs7")
        encrypted = cipher.encrypt(padPkcs7)
        return [encrypted[i] for i in range(len(encrypted))]

    @logger.catch
    def Encrypt(self, dic: dict) -> str:
        params = json.dumps(dic)

        # u = xxxxx
        u = self.RSA(self.aeskey.decode())
        # h = [116,13,253,xxxxxxxxxxxxxxxx,70,100]
        h = self.AES(data=params)
        # aewrhtjyksudlyi;ulkutyjrhtegwfqed eergtyg
        p = GeetestBase().enc(h)
        w = p + u
        return w

    @logger.catch
    def ClickCalculate(self) -> str:
        passtime = random.randint(1300, 2000)

        m5 = md5()
        m5.update((self.gt + self.challenge[:-2] + str(passtime)).encode())
        rp = m5.hexdigest()

        dic = {
            "lang": "zh-cn",
            "passtime": passtime,
            "a": self.key,  # 点选位置, e
            "tt": "",  # tt_c
            "ep": {
                "v": "9.1.8-bfget5",
                "$_E_": False,
                "me": True,
                "ven": "Google Inc. (Intel)",
                "ren": "ANGLE (Intel, Intel(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0, D3D11)",
                "fp": ["move", 483, 149, 1702019849214, "pointermove"],
                "lp": ["up", 657, 100, 1702019852230, "pointerup"],
                "em": {
                    "ph": 0,
                    "cp": 0,
                    "ek": "11",
                    "wd": 1,
                    "nt": 0,
                    "si": 0,
                    "sc": 0,
                },
                "tm": {
                    "a": 1702019845759,
                    "b": 1702019845951,
                    "c": 1702019845951,
                    "d": 0,
                    "e": 0,
                    "f": 1702019845763,
                    "g": 1702019845785,
                    "h": 1702019845785,
                    "i": 1702019845785,
                    "j": 1702019845845,
                    "k": 1702019845812,
                    "l": 1702019845845,
                    "m": 1702019845942,
                    "n": 1702019845946,
                    "o": 1702019845954,
                    "p": 1702019846282,
                    "q": 1702019846282,
                    "r": 1702019846287,
                    "s": 1702019846288,
                    "t": 1702019846288,
                    "u": 1702019846288,
                },
                "dnf": "dnf",
                "by": 0,
            },
            "h9s9": "1816378497",
            "rp": rp,
        }
        return self.Encrypt(dic)

    @logger.catch
    def SlideCalculate(self) -> str:
        passtime = random.randint(1300, 2000)

        m5 = md5()
        m5.update((self.gt + self.challenge[:-2] + str(passtime)).encode())
        rp = m5.hexdigest()

        """
        track = [
            [-33, -36, 0],
            [0, 0, 0],
            [1, 0, 6],
            [2, 0, 30],
            [2, -1, 38],
            [4, -1, 134],
            [4, -1, 159],
            [4, -1, 239],
        ]
        """

        dic = {
            "lang": "zh-cn",
            # userresponse(self.key +  challenge)
            "userresponse": "",
            # n=消耗时间
            "passtime": passtime,
            # 加载数据
            "imgload": random.randint(70, 150),
            # aa(track, self.c, self.s),
            "aa": "",
            "ep": {
                "v": "7.9.2",
                "$_BIE": False,
                "me": True,
                "tm": {
                    "a": 1720326755214,
                    "b": 0,
                    "c": 0,
                    "d": 0,
                    "e": 0,
                    "f": 1720326755214,
                    "g": 1720326755214,
                    "h": 1720326755214,
                    "i": 1720326755309,
                    "j": 1720326755685,
                    "k": 1720326755310,
                    "l": 1720326755685,
                    "m": 1720326756051,
                    "n": 1720326756051,
                    "o": 1720326756080,
                    "p": 1720326756689,
                    "q": 1720326756689,
                    "r": 1720326756694,
                    "s": 1720326756694,
                    "t": 1720326756694,
                    "u": 1720326756695,
                },
                "td": -1,
            },
            "h9s9": "1816378497",
            "rp": rp,
        }
        return self.Encrypt(dic)
