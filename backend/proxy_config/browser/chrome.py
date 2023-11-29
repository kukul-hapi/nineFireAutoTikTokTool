import random
import time





def is_port_in_use(port):
    import psutil
    for connection in psutil.net_connections():
        if connection.laddr.port == port and connection.status == psutil.CONN_LISTEN:
            return True
    return False


PORT_RANGE_START = 4600
PORT_RANGE_END = 4699


def generate_port():
    import threading
    port_lock = threading.Lock()
    port = 0
    established = False
    with port_lock:
        while not established:
            port = random.choice(range(PORT_RANGE_START, PORT_RANGE_END))
            if not is_port_in_use(port):
                established = True
    return port

def chrome_setup(email_account,lock):
    from selenium import webdriver
    import undetected_chromedriver as uc
    from proxy_config.models import DvadminSystemTiktokProxyConfig
    import requests
    proxy_config = DvadminSystemTiktokProxyConfig.objects.get(id=email_account.proxy_id)
    local_port = proxy_config.local_port
    options = uc.ChromeOptions()
    # options.add_experimental_option('excludeSwitches',
    #                                 ['enable-automation'])
    options.add_argument(
        f"--remote-debugging-port-{str(local_port)}")
    options.add_argument("--no-sandbox")
    open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + email_account.bro_id
    try:
        time.sleep(1)
        print("请求 "+email_account.username)
        with lock:
         resp = requests.get(open_url).json()
        print(resp)
        chrome_driver = resp["data"]["webdriver"]
        options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
        driver = webdriver.Chrome(
            chrome_driver,
            options=options
        )
    except Exception as e:
        print(f"Error while creating WebDriver: {e}")
    finally:
        return driver
