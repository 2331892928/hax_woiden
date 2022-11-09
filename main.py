import os
import time

import ddddocr
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By

# ----------------配置区-------------------#
#  每7天续约一次，建议本脚本执行频率高一些，不仅可以cookie保活，也能防止ocr失败验证码的失败或连接超时导致服务器续签失败。推荐1小时一次
# 你的cookie。两个站的cookie是分开的
Cookie2 = "ki2fc7caa7fg6d75tb3kd2rbb7"
#  谷歌驱动，仅支持谷歌浏览器，请下载对应的selenium驱动
webdriver_qd = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe"
# woiden.id或hax.co.id
Domain = "woiden.id"
TimeOut = 120


# ----------------配置区-------------------#

class Woiden:
    def __init__(self):
        self.renew_href = "https://woiden.id/renew-vps-process/"
        self.renew_html = "https://woiden.id/vps-renew/"
        self.headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://woiden.id",
            "referer": "https://woiden.id/vps-renew/",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"}
        self.cookie = {
            # "PHPSESSID": Cookie,
            "PHPSESSID": Cookie2
        }

    #  已被弃用：原因，谷歌无感验证码已获取，但平台不认，可能有内部沟通:平台->谷歌验证码->平台->谷歌验证码。
    def sign(self):
        # cookie保活并检查cookie是否有效，如果有效，提取验证码
        res = requests.get(self.renew_html, cookies=self.cookie, headers=self.headers)
        restxt = res.content.decode()
        if restxt.find("logout") == -1:
            print("cookie已失效")
            return None
        return "1"
        # soup = bs4.BeautifulSoup(restxt, "html.parser")
        # 提取验证码token
        # token = requests.get(
        #     "https://recaptcha.net/recaptcha/api2/anchor?ar=1&k=6LccKFofAAAAALd8cedymUD1TUWgzTLWKsdlqc-8&co=aHR0cHM6Ly93b2lkZW4uaWQ6NDQz&hl=zh-CN&v=Ixi5IiChXmIG6rRkjUa1qXHT&size=invisible",
        #     self.headers)
        # soup1 = bs4.BeautifulSoup(token.content.decode(), "html.parser")
        # token = soup1.find("input", attrs={"id": "recaptcha-token"})['value']
        #
        # # 提取验证码
        # form = soup.find_all("form", attrs={"id": "form-submit"})
        # col = form[0].find("div", attrs={"class": "col-sm-3"})
        # # 验证码是算数分开，先提取算术符号
        # arithmeticCharacter = col.contents[2]
        # #  图片链接
        # img1 = col.contents[1]['src']
        # img2 = col.contents[3]['src']
        # #  放入文件
        # with open("./img1.jpg", "wb") as f:
        #     f.write(requests.get(img1).content)
        # with open("./img2.jpg", "wb") as f:
        #     f.write(requests.get(img2).content)
        # dddocr = ddddocr.DdddOcr()
        # #  识别验证码图片
        # img1 = dddocr.classification(open('./img1.jpg', 'rb').read())
        # img2 = dddocr.classification(open('./img2.jpg', 'rb').read())
        # #  删除验证码图片
        # if os.path.exists("./img1.jpg"):
        #     os.remove("./img1.jpg")
        # if os.path.exists("./img2.jpg"):
        #     os.remove("./img2.jpg")
        # arithmeticCharacter = str(arithmeticCharacter)
        # print("验证码获取成功")
        # yzmstr = img1 + arithmeticCharacter + img2 + "={}"
        # try:
        #     if arithmeticCharacter.lower() == "+":
        #         yzm = int(img1) + int(img2)
        #         print(yzmstr.format(yzm))
        #     elif arithmeticCharacter.lower() == "-":
        #         yzm = int(img1) - int(img2)
        #         print(yzmstr.format(yzm))
        #     elif arithmeticCharacter.lower() == "x":
        #         yzm = int(img1) * int(img2)
        #         print(yzmstr.format(yzm))
        #     else:
        #         yzm = int(img1) / int(img2)
        #         print(yzmstr.format(yzm))
        # except:
        #     yzm = 0
        #     print("ocr失败")
        #     print(yzmstr.format(yzm))
        # return [token, yzm]

    def renew(self, token, yzm):
        submit = {
            "action": "renew_vps",
            "token": token,
            "web_address": "woiden.id",
            "captcha": yzm,
            "agreement": "yes",
        }
        self.cookie['_GRECAPTCHA'] = token
        # print(submit)
        res = requests.post(self.renew_href, cookies=self.cookie, data=submit, headers=self.headers)
        print(res.content.decode())

    def renewv2(self):
        # 验证cookie是否可用
        if self.sign() is None:
            print("cookie失效")
            return None
        drive = webdriver.Edge(executable_path=webdriver_qd)
        drive.set_page_load_timeout(TimeOut)
        drive.maximize_window()
        #  将普通cookie变成浏览器cookie
        drive.get("https://{}/vps-renew/".format(Domain))
        drive.delete_all_cookies()
        for i, v in enumerate(self.cookie):
            drive.add_cookie({"name": v, "value": self.cookie[v], "domain": Domain})
        time.sleep(3)
        drive.get("https://{}/vps-renew/".format(Domain))
        time.sleep(3)
        drive.refresh()

        # 阻塞，打开完成才执行下面
        while True:
            restxt = drive.page_source
            soup = bs4.BeautifulSoup(restxt, "html.parser")

            # 提取验证码
            form = soup.find_all("form", attrs={"id": "form-submit"})
            col = form[0].find("div", attrs={"class": "col-sm-3"})
            # 验证码是算数分开，先提取算术符号
            arithmeticCharacter = col.contents[2]
            #  图片链接
            img1 = col.contents[1]['src']
            img2 = col.contents[3]['src']
            #  放入文件
            with open("./img1.jpg", "wb") as f:
                f.write(requests.get(img1).content)
            with open("./img2.jpg", "wb") as f:
                f.write(requests.get(img2).content)
            dddocr = ddddocr.DdddOcr()
            #  识别验证码图片
            img1 = dddocr.classification(open('./img1.jpg', 'rb').read())
            img2 = dddocr.classification(open('./img2.jpg', 'rb').read())
            #  删除验证码图片
            if os.path.exists("./img1.jpg"):
                os.remove("./img1.jpg")
            if os.path.exists("./img2.jpg"):
                os.remove("./img2.jpg")
            arithmeticCharacter = str(arithmeticCharacter)
            print("验证码获取成功")
            yzmstr = img1 + arithmeticCharacter + img2 + "={}"
            try:
                if arithmeticCharacter.lower() == "+":
                    yzm = int(img1) + int(img2)
                    print(yzmstr.format(yzm))
                elif arithmeticCharacter.lower() == "-":
                    yzm = int(img1) - int(img2)
                    print(yzmstr.format(yzm))
                elif arithmeticCharacter.lower() == "x":
                    yzm = int(img1) * int(img2)
                    print(yzmstr.format(yzm))
                else:
                    yzm = int(img1) / int(img2)
                    print(yzmstr.format(yzm))
                break
            except:
                # 识别失败，重新识别
                print("验证码识别失败,刷新重新识别")
                time.sleep(3)
                drive.refresh()
        # 填写
        print("填写domain")
        drive.find_element(By.ID, "web_address").send_keys(Domain)
        print("填写验证码")
        drive.find_element(By.ID, "captcha").send_keys(yzm)
        print("点击协议")
        drive.find_element(By.CLASS_NAME, "form-check-input").click()
        print("提交")
        drive.find_element(By.NAME, "submit_button").click()
        # 等待服务器响应后
        i = 0
        for i in range(0, TimeOut):
            if drive.page_source.find("Your VPS has") != -1:
                break
            time.sleep(1)

        if i < TimeOut - 1:
            print("续签成功")
        else:
            print("续签失败")
        drive.close()

        #  一直阻塞到脚本执行完毕


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    W = Woiden()
    W.renewv2()
    # yz = W.sign()
    # W.renew(yz[0], yz[1])

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
