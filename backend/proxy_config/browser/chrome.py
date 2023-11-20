from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import random
import time

# Headless mode - the application is working without an UI - only in the backend
### Recommended for the bulk methods we will be using ###
#


def get_proxies():
    from selenium.webdriver.common.by import By
    import undetected_chromedriver as uc

    ops = uc.ChromeOptions()
    ops.add_argument("--headless")
    driver = uc.Chrome(ops)
    driver.get("https://free-proxy-list.net/")

    proxies = []

    proxy_table_rows = driver.find_elements(By.XPATH, '//table/tbody/tr')

    for p in range(1, len(proxy_table_rows)):
        if proxy_table_rows[p].text.split(' ')[5] == 'yes':
            proxies.append(proxy_table_rows[p].text.split(
                ' ')[0] + ':' + proxy_table_rows[p].text.split(' ')[1])
    driver.close()

    return proxies


def is_port_in_use(port):
    import psutil
    for connection in psutil.net_connections():
        if connection.laddr.port == port and connection.status == psutil.CONN_LISTEN:
            return True
    return False

# Generating and checking a free port for running multiple drivers simultaneously
# with port_lock:
#     bro_id = email_account.bro_id
#     port = generate_port()
#     # 如果bro_id为空，调用self.createBro()并保存返回值
#     if not bro_id:
#         email_account = self.createBro(email_account)
#         # bro_id不为空，调用self.TikTokRegister
#         email_account.local_port = port
#     self.TikTokRegister(bro_id)
PORT_RANGE_START = 4600
PORT_RANGE_END = 4699
import threading
port_lock = threading.Lock()
def generate_port():
    port = 0
    established = False
    with port_lock:
        while not established:
            port = random.choice(range(PORT_RANGE_START, PORT_RANGE_END))
            if not is_port_in_use(port):
                established = True
    return port

def chrome_setup(email_account):
    from selenium import webdriver
    import undetected_chromedriver as uc
    from proxy_config.models import DvadminSystemTiktokProxyConfig
    import requests
    proxy_config = DvadminSystemTiktokProxyConfig.objects.get(id=email_account.proxy_id)
    local_port = proxy_config.local_port
    options = uc.ChromeOptions()
    options.add_argument(
        f"--remote-debugging-port-{str(local_port)}")
    options.add_argument("--no-sandbox")
    open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + email_account.bro_id
    resp = requests.get(open_url).json()
    chrome_driver = resp["data"]["webdriver"]
    options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
    driver = webdriver.Chrome(
        chrome_driver,
        options=options
    )
    return driver
