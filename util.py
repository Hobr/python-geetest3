import json
import random
from binascii import hexlify
from hashlib import md5

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from loguru import logger


class GeetestBase:
    CUSTOM_BASE64_ALPHABET = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()"
    )

    _PART1_BITS = [22, 21, 19, 18, 17, 16]
    _PART2_BITS = [23, 20, 15, 13, 12, 10]
    _PART3_BITS = [14, 11, 9, 8, 4, 2]
    _PART4_BITS = [7, 6, 5, 3, 1, 0]

    def _get_base64_char(self, index: int) -> str:
        return (
            self.CUSTOM_BASE64_ALPHABET[index]
            if 0 <= index < len(self.CUSTOM_BASE64_ALPHABET)
            else "."
        )

    @staticmethod
    def _extract_bits(value: int, bits: list) -> int:
        result = 0
        for bit in bits:
            result = (result << 1) | ((value >> bit) & 1)
        return result

    def enc(self, data: bytes) -> str:
        encoded = []
        padding = ""
        for i in range(0, len(data), 3):
            chunk = data[i : i + 3]
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
            else:
                remainder = len(chunk)
                c = chunk[0] << 16
                if remainder == 2:
                    c |= chunk[1] << 8
                encoded.append(
                    self._get_base64_char(self._extract_bits(c, self._PART1_BITS))
                )
                encoded.append(
                    self._get_base64_char(self._extract_bits(c, self._PART2_BITS))
                )
                if remainder == 2:
                    encoded.append(
                        self._get_base64_char(self._extract_bits(c, self._PART3_BITS))
                    )
                    padding = "."
                else:
                    padding = ".."
        return "".join(encoded) + padding


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
        u = self.RSA(self.aeskey.decode())
        h = self.AES(data=params)
        p = GeetestBase().enc(bytes(h))
        return p + u

    @logger.catch
    def ClickCalculate(self) -> str:
        passtime = random.randint(1300, 2000)
        m5 = md5()
        m5.update((self.gt + self.challenge[:-2] + str(passtime)).encode())
        rp = m5.hexdigest()

        dic = {
            "lang": "zh-cn",
            "passtime": passtime,
            # 点选位置, e
            "a": self.key,
            # tt_c
            "tt": "",
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
