import bili_ticket_gt_python
import time

from util import W
import httpx

click = bili_ticket_gt_python.ClickPy()
slide = bili_ticket_gt_python.SlidePy()

for _i in range(50):
    try:
        # Click
        print("----------点字----------")

        (gt, challenge) = click.register_test(
            "https://passport.bilibili.com/x/passport-login/captcha?source=main_web"
        )
        (_, _) = click.get_c_s(gt, challenge)
        _type = click.get_type(gt, challenge)

        if _type != "click":
            raise Exception("验证码类型错误")

        (c, s, args) = click.get_new_c_s_args(gt, challenge)

        before_calculate_key = time.time()
        key = click.calculate_key(args)

        w = W(key=key, gt=gt, challenge=challenge, c=str(c), s=s).ClickCalculate()
        print(f"key: {key}, gt: {gt}, challenge: {challenge}, c: {c}, s: {s}, w: {w}")

        w_use_time = time.time() - before_calculate_key
        print(f"w生成时间: {w_use_time}")
        if w_use_time < 2:
            time.sleep(2 - w_use_time)

        (msg, validate) = click.verify(gt, challenge, w)
        print(f"{msg} {validate}")

        time.sleep(3)

        # Slide https://bili2233.cn/TJJxeHH
        print("----------滑块----------")
        data = {
            "customerId": "",
            "deviceId": "ad86110dee0d4eea60cfc9c2e2f7d7ae",
            "voucher": "alsfn234nlasf",
            "clientType": "h5",
            "csrf": "3fe94ee3c56c03582988ce62d3c028bd",
        }
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Content-Type": "application/json",
            "Referer": "https://mall.bilibili.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }
        res = httpx.post(
            url="https://show.bilibili.com/open/verify/geetest/get?oaccesskey=",
            json=data,
            headers=header,
        )

        if res.status_code != httpx.codes.OK:
            res.raise_for_status()

        res = res.json().get("data")

        gt = res["captcha_id"]
        challenge = res["challenge"]

        (_, _) = slide.get_c_s(gt, challenge)
        _type = slide.get_type(gt, challenge)

        if _type != "slide":
            raise Exception("验证码类型错误")

        (c, s, args) = slide.get_new_c_s_args(gt, challenge)

        before_calculate_key = time.time()
        challenge = args[0]
        key = slide.calculate_key(args)

        w = W(key=key, gt=gt, challenge=challenge, c=str(c), s=s).SlideCalculate()
        print(f"key: {key}, gt: {gt}, challenge: {challenge}, c: {c}, s: {s}, w: {w}")

        w_use_time = time.time() - before_calculate_key
        print(f"w生成时间: {w_use_time}")
        if w_use_time < 2:
            time.sleep(2 - w_use_time)

        (msg, validate) = slide.verify(gt, challenge, w)
        print(f"{msg} {validate}")

    except Exception as e:
        print("识别失败")
        print(e)
