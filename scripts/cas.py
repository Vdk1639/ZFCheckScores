from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import time

# === 账号密码 ===
'''从环境变量中获取账号密码和CAS登录URL'''
'''CAS_url = os.environ.get("URL")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")'''

def CAS_login(CAS_url, username, password):
    """
    使用Selenium自动登录CAS统一身份认证页面并返回登录后的WebDriver实例。
    :param CAS_url: CAS登录URL
    :param USERNAME: 用户名
    :param PASSWORD: 密码
    :return: 登录成功的WebDriver实例
    :rtype: selenium.webdriver.Chrome
    """
    # === 启动浏览器 ===
    driver = webdriver.Chrome()
    driver.get(CAS_url)
    # === 等待页面加载设置超时时间10秒 ===
    wait = WebDriverWait(driver, 10)
    # === 自动填写账号密码（CAS 统一身份认证页面）===
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.NAME, "passwordText"))).send_keys(password)
    # === 提交登录表单（回车） ===
    wait.until(EC.element_to_be_clickable((By.NAME, "passwordText"))).send_keys(Keys.RETURN)
    # === 等待登录完成 ===
    title = driver.title
    if title=='信息门户':
        print("登录成功，当前页面标题为：", title)
        return driver
    else:
        attempts = 5  # 最大重试次数
        while attempts > 0:
            print('标题',title,'不正确，正在重试...')
            time.sleep(1)
            title = driver.title
            if title == '信息门户':
                print("登录成功，当前页面标题为：", title)
                return driver
            attempts -= 1
        # 如果重试后仍未成功，打印错误信息
        print("登录失败，当前页面标题为：", title)
        return None

def jump2jwxt(driver):
    """
    在登录后的WebDriver实例中，跳转到教务系统模块。
    :param driver: 登录后的WebDriver实例
    """
    # 等待 iframe 加载完成
    wait = WebDriverWait(driver, 10)
    iframe = wait.until(EC.presence_of_element_located((By.ID, "template-container")))
    # 切换到包含“教务系统”模块的 iframe
    # 注意：这里只有一个 iframe，所以直接使用xpath定位
    driver.switch_to.frame(iframe)
    # 等待“教务系统”模块出现并可点击
    target = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@servicename='教务系统']")))
    # 点击它
    target.click()
    # 等待新窗口打开
    wait.until(EC.number_of_windows_to_be(2))
    # 切换到刚打开的标签页
    driver.switch_to.window(driver.window_handles[-1])
    driver.current_window_handle
    # 获取当前页面标题
    title = driver.title
    #print(title)
    if title=="教学管理信息服务平台":
        print("教务登录成功，当前页面标题为：", title)
        return driver
    else:
        attempts = 5  # 最大重试次数
        while attempts > 0:
            print('标题',title,'不正确，正在重试...')
            time.sleep(1)
            title = driver.title
            if title == '教学管理信息服务平台':
                print("登录成功，当前页面标题为：", title)
                return driver
            attempts -= 1
        print("教务登录失败，当前页面标题为：", title)
        return None
    
def main(cas_url=None, username=None, password=None):
    """ 主函数，执行登录和跳转到教务系统的操作。
    :param cas_url: CAS登录URL
    :param username: 用户名
    :param password: 密码
    """
    try:
        driver=CAS_login(cas_url, username, password)
    except Exception as e:
        print(f"登录过程中发生错误: {e}")
    else:
        print("登录成功，正在跳转到教务系统...")
        try:
            # 跳转到教务系统
            driver = jump2jwxt(driver)
        except Exception as e:
            print(f"跳转到教务系统时发生错误: {e}")
            return None
        else:
            # 获取 selenium 中的 cookies
            selenium_cookies = driver.get_cookies()
            # 获取当前标签页的URL（即教务系统的URL）
            jwxt_url = driver.current_url
            print(f"获取到的成绩页面URL: {jwxt_url}")
            # 创建一个 requests 会话
            session = requests.Session()
            # 设置与浏览器相同的请求头，增加请求的伪装性
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
            })

            # 将 selenium 的 cookies 复制到 requests 会话中
            for cookie in selenium_cookies:
                session.cookies.set(cookie['name'], cookie['value'])
            # 访问教务系统页面
            print(f"正在访问教务页面: {jwxt_url}")
            response = session.get(jwxt_url)
            return response.status_code, response, session

if __name__ == "__main__":
    '''本地测试没有设置环境变量，直接在读取填写账号密码和CAS登录URL'''
    CAS_url = "https://webvpn.njrts.edu.cn/"
    with open("config.txt", "r") as f:
        lines = f.readlines()
        USERNAME = lines[0].strip()  # 第一行是用户名
        PASSWORD = lines[1].strip()  # 第二行是密码
    status_code, response, session=main(CAS_url, USERNAME, PASSWORD)