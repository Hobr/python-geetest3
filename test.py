import bili_ticket_gt_python
import time

from util import W

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
        print(w)

        w_use_time = time.time() - before_calculate_key
        print(f"w生成时间: {w_use_time}")
        if w_use_time < 2:
            time.sleep(2 - w_use_time)

        (msg, validate) = click.verify(gt, challenge, w)
        print(f"{msg} {validate}")

        time.sleep(3)

        # Slide
        print("----------滑块----------")

        (gt, challenge) = slide.register_test("https://bili2233.cn/TJJxeHH")
        (_, _) = slide.get_c_s(gt, challenge)
        _type = slide.get_type(gt, challenge)

        if _type != "slide":
            raise Exception("验证码类型错误")

        (c, s, args) = slide.get_new_c_s_args(gt, challenge)

        before_calculate_key = time.time()
        challenge = args[0]
        key = slide.calculate_key(args)

        w = W(key=key, gt=gt, challenge=challenge, c=str(c), s=s).SlideCalculate()
        print(w)

        w_use_time = time.time() - before_calculate_key
        print(f"w生成时间: {w_use_time}")
        if w_use_time < 2:
            time.sleep(2 - w_use_time)

        (msg, validate) = slide.verify(gt, challenge, w)
        print(f"{msg} {validate}")

    except Exception as e:
        print("识别失败")
        print(e)
