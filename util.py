import json
import random
from binascii import hexlify
from hashlib import md5

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from loguru import logger


class Track:
    @logger.catch
    def enc(self, track: list, c: str, s: str) -> str:
        return self.SecondEnc(self.FirstEnc(track), c, s)

    @logger.catch
    def FirstEnc(self, mousetrack: list):
        def n(t):
            e = "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqr"
            n_len = len(e)
            r = ""
            i = abs(t)
            o = int(i / n_len)
            if n_len <= o:
                o = n_len - 1
            if o:
                r = e[o]
            s = ""
            if t < 0:
                s += "!"
            if r:
                s += "$"
            s += e[i % n_len]
            return s

        def find_special_point(t):
            special_points = [
                [1, 0],
                [2, 0],
                [1, -1],
                [1, 1],
                [0, 1],
                [0, -1],
                [3, 0],
                [2, -1],
                [2, 1],
            ]
            for sp in special_points:
                if t[0] == sp[0] and t[1] == sp[1]:
                    return "stuvwxyz~"[special_points.index(sp)]
            return 0

        def track_transform(t):
            i = []
            for s in range(len(t) - 1):
                e = round(t[s + 1][0] - t[s][0])
                n = round(t[s + 1][1] - t[s][1])
                # r = round(t[s + 1][2] - t[s][2])
                o = 0
                if e != 0:
                    o = e
                i.append([e, n, o])
            return i

        t = track_transform(mousetrack)
        r = []
        i = []
        o = []
        for point in t:
            e = find_special_point(point)
            if e:
                i.append(e)
            else:
                r.append(n(point[0]))
                i.append(n(point[1]))
            o.append(n(point[2]))
        return "".join(r) + "!!" + "".join(i) + "!!" + "".join(o)

    @logger.catch
    def SecondEnc(self, t, e: str, n: str) -> str:
        i = 0
        o = t
        s = e[0]
        a = e[2]
        _ = e[4]

        while i < len(n):
            r = n[i : i + 2]
            i += 2
            c = int(r, 16)
            u = chr(c)
            ll = (s * c * c + a * c + _) % len(t)
            o = o[:ll] + u + o[ll:]
        return o


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
    def __ease_out_expo(self, sep: float) -> float:
        """
        缓动函数 easeOutExpo
        参考: https://easings.net/zh-cn#easeOutExpo
        """
        if sep == 1:
            return 1
        else:
            return 1 - pow(2, -10 * sep)

    @logger.catch
    def get_slide_track(self, distance: int) -> list:
        """
        根据滑动距离生成滑动轨迹
        :param distance: 需要滑动的距离
        :return: 滑动轨迹<type 'list'>: [[x,y,t], ...]
            x: 已滑动的横向距离
            y: 已滑动的纵向距离, 除起点外, 均为0
            t: 滑动过程消耗的时间, 单位: 毫秒
        """

        if not isinstance(distance, int) or distance < 0:
            raise ValueError(
                f"distance类型必须是大于等于0的整数: distance: {distance}, type: {type(distance)}"
            )
        # 初始化轨迹列表
        slide_track = [
            [random.randint(-50, -10), random.randint(-50, -10), 0],
            [0, 0, 0],
        ]
        # 共记录count次滑块位置信息
        count = 30 + int(distance / 2)
        # 初始化滑动时间
        t = random.randint(50, 100)
        # 记录上一次滑动的距离
        _x = 0
        _y = 0
        for i in range(count):
            # 已滑动的横向距离
            x = round(self.__ease_out_expo(i / count) * distance)
            # 滑动过程消耗的时间
            t += random.randint(10, 20)
            if x == _x:
                continue
            slide_track.append([x, _y, t])
            _x = x
        slide_track.append(slide_track[-1])
        return slide_track

    @logger.catch
    def ClickCalculate(self) -> str:
        passtime = random.randint(1300, 2000)
        m5 = md5()
        m5.update((self.gt + self.challenge[:-2] + str(passtime)).encode())
        rp = m5.hexdigest()

        dic = {
            "lang": "zh-cn",
            "passtime": passtime,
            # 点选位置
            "a": self.key,
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
        # 滑动时间: track[track.length - 1][2]
        passtime = random.randint(1300, 2000)
        m5 = md5()
        m5.update((self.gt + self.challenge[:-2] + str(passtime)).encode())
        rp = m5.hexdigest()

        dic = {
            "lang": "zh-cn",
            # 滑动距离 + challenge
            "userresponse": self.key + self.challenge,
            "passtime": passtime,
            "imgload": random.randint(100, 200),
            # 轨迹加密
            "aa": "",
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
            "rp": rp,
        }

        return self.Encrypt(dic)
