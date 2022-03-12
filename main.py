from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from secret import Zyh, Lx  # username and password
from alive_progress import alive_it
from random import randint
from rich import print

timeout = 5

options = webdriver.EdgeOptions()
options.add_argument("headless")
# options = webdriver.ChromeOptions()
# options.add_argument("-headless")

driver = webdriver.Edge(options=options)
# driver = webdriver.Chrome(options=options)
print(driver)
driver.implicitly_wait(timeout)

magic_words = "main/article"
tracing = False
user = Zyh


def restart():
    global driver
    print("[r]RESTARTING")
    driver = webdriver.Edge(options=options)
    # driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(timeout)


def login():
    driver.get("https://xgfx.bnuz.edu.cn/xsdtfw/sys/emapfunauth/pages/welcome.do#/")

    click_by_xpaths("/html/body/div[1]/div/div/div/div/button[2]")
    driver.find_element(
        By.XPATH,
        '//*[@id="emap-rsids-content"]/div/div[3]/div/div[1]/div/div[1]/div/input'
    ).send_keys(user.username)
    driver.find_element(
        By.XPATH,
        '//*[@id="emap-rsids-content"]/div/div[3]/div/div[2]/div/div[1]/div/input'
    ).send_keys(user.password)


def click_by_xpaths(*xpaths):
    for xpath in xpaths:
        driver.find_element(By.XPATH, xpath).click()


def send_by_xpath(xpath, text, select=False):
    box = driver.find_element(By.XPATH, xpath)
    if select:
        box.send_keys(Keys.CONTROL + "A")
    box.send_keys(text)


def input_temperature():
    ans = randint(363, 371) / 10
    print(f"today's body temperature is {ans}℃")
    send_by_xpath(
        f'/html/body/{magic_words}/section/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/input',
        str(ans)
    )


def choose_false(n):
    for n in range(n):
        click_by_xpaths(
            f'/html/body/{magic_words}/section/div[2]/div[2]/div/div[2]/div[2]/div[{6 + 2 * n}]/div/div/div[2]/div/div/div[1]',
            f'/html/body/div[{24 + tracing * 5 + 2 * n}]/div/div/div/div[2]/div/div[3]/span'
        )


def fill_all():
    input_temperature()
    choose_false(5)
    click_by_xpaths('//*[@id="save"]')


def get_before(n):
    from datetime import date, timedelta
    return f"{date.today() - timedelta(n):%Y-%m-%d}"


def get_text(date):
    # return "测试"
    import arrow
    now = arrow.now()
    return f"""\
现在是{now}
正在填写{date}即{arrow.get(date).humanize()}的健康打卡
链接
https://github.com/CNSeniorious000/project_automata\n以下是800个随机数字\n""" + "".join(str(randint(1,9)) for _ in range(800))


def trace(past):
    global magic_words, tracing
    magic_words = "div[11]/div/div[1]"
    tracing = True
    for i in alive_it(past):
        date = get_before(i)
        print(date)
        try:
            click_by_xpaths('//*[@id="mrbpaxz-bl"]')  # 补录
            text = get_text(date)
            if text:
                print(text)
                input_bonus(text)
            send_by_xpath(
                '/html/body/div[11]/div/div[1]/section/div[2]/div[2]/div/div[2]/div[2]/div[1]/div/div/div[2]/input',
                date + "\n", select=True
            )
            fill_all()
        except BaseException as ex:
            print(f"[r]{type(ex).__name__}")
            return i


def prepare():
    login()
    page = driver.current_window_handle
    click_by_xpaths(
        '//*[@id="emap-rsids-content"]/div/div[3]/div/div[3]/div/button/span',  # 登录
        '/html/body/main/article/section[1]/div/div/div/div[1]/div/div[2]/span',  # 疫情返校
        '/html/body/main/article/section[1]/div/div/div/div[2]/div[2]/div/div[2]',  # 疫情自查上报
    )
    driver.switch_to.window([handle for handle in driver.window_handles if handle != page][0])


def robust_trace_range(start, end, step=1):
    i = start
    prepare()
    while True:
        try:
            i = trace(range(i, end, step)) + step
            print(f"[r]{i = }")
        except TypeError:
            return
        try:
            # click_by_xpaths(
            #     '/html/body/div[39]/div[1]/div[1]/div[2]/div[2]/a',
            #     '/html/body/main/article/h2'
            # )
            driver.refresh()
        except BaseException as ex:
            print(f"[r]{ex}")
            restart()
            prepare()

def main():
    prepare()
    fill_all()


def input_bonus(text):
    send_by_xpath(
        f'/html/body/{magic_words}/section/div[2]/div[1]/div/div[1]/div[2]/div[25]/div/div/div[2]/div/textarea',
        text, select=True
    )


if __name__ == '__main__':
    import sys

    print(sys.argv[1:])
    if "lx" in sys.argv:
        user = Lx
    if "main" in sys.argv:
        sys.exit(main())
    else:
        robust_trace_range(*map(int, sys.argv[1:4]))
