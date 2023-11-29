from selenium.common import TimeoutException
from lxml import etree
from proxy_config.models import DvadminSystemUserEmail, DvadminSystemTiktokProxyConfig
from proxy_config.utils.serializers import TKUserEmailModelSerializer, TKUserEmailModelCreateUpdateSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from rest_framework.decorators import action
from dvadmin.utils.json_response import DetailResponse
from loguru import logger
from proxy_config.browser.chrome import chrome_setup, generate_port
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import time
import random
from rest_framework import serializers
from proxy_config.utils.random_email_name.randoms import EmailNameGenerator


class ExportAccountProfileSerializer(CustomModelSerializer):
    last_login = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True
    )
    is_active = serializers.SerializerMethodField(read_only=True)
    dept_name = serializers.CharField(source="dept.name", default="")
    dept_owner = serializers.CharField(source="dept.owner", default="")
    gender = serializers.CharField(source="get_gender_display", read_only=True)


class TKUserEmailModelViewSet(CustomModelViewSet):
    """
    配置参数接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = DvadminSystemUserEmail.objects.all()
    serializer_class = TKUserEmailModelSerializer
    create_serializer_class = TKUserEmailModelCreateUpdateSerializer
    update_serializer_class = TKUserEmailModelCreateUpdateSerializer
    filter_fields = ['desc_name', 'username', 'fans_count', 'video_count', 'proxy_address', 'mari_dir',
                     'update_datetime',
                     'is_active', 'account_type', 'description', 'account_state']
    search_fields = ['username']
    # 导出
    export_field_label = {
        "username": "用户账号",
        "IP": "IP",
        "type": "类型",
        "port": "端口",
        "password": "密码",
        "is_active": "帐号状态",
        "local_proxy_port_traffic": "本地代理端口流量统计",
        "local_port": "本地端口"
    }
    export_serializer_class = ExportAccountProfileSerializer

    @action(methods=["POST"], detail=False)
    def enable_list(self, request):
        # 获取要批量修改的记录
        records_to_enable = DvadminSystemUserEmail.objects.all()
        # 批量修改记录的状态
        for record in records_to_enable:
            print(f'Record ID: {record.id}, is_active: {record.is_active}')
            record.is_active = 1  # 假设修改状态字段为 is_active
            record.save()
        return DetailResponse(msg="修改成功")

    @action(methods=["POST"], detail=False)
    def disable_list(self, request):
        # 获取要批量修改的记录
        records_to_enable = DvadminSystemUserEmail.objects.all()
        # 批量修改记录的状态
        for record in records_to_enable:
            print(f'Record ID: {record.id}, is_active: {record.is_active}')
            record.is_active = 0  # 假设修改状态字段为 is_active
            record.save()

        return DetailResponse(msg="修改成功")

    @action(methods=["POST"], detail=False)
    def enable_on_page(self, request):
        # 获取要批量修改的记录
        page = int(request.query_params.get('page'))  # 获取页码参数，默认为 1
        page_size = int(request.query_params.get('limit'))  # 获取每页数量参数，默认为 20

        # 根据页码和每页数量计算查询的起始和结束索引
        start_index = (page - 1) * page_size
        end_index = page * page_size

        print(start_index, end_index)
        # 获取要批量修改的记录
        records_to_enable = DvadminSystemUserEmail.objects.all()[start_index:end_index]
        # 批量修改记录的状态
        for record in records_to_enable:
            print(f'Record ID: {record.id}, is_active: {record.is_active}')
            record.is_active = 1  # 假设修改状态字段为 is_active
            record.save()

        return DetailResponse(msg="修改成功")



    @action(methods=["POST"], detail=False)
    def disable_on_page(self, request):
        page = int(request.query_params.get('page'))  # 获取页码参数，默认为 1
        page_size = int(request.query_params.get('limit'))  # 获取每页数量参数，默认为 20
        # 根据页码和每页数量计算查询的起始和结束索引
        start_index = (page - 1) * page_size
        end_index = page * page_size
        # 获取要批量修改的记录
        records_to_enable = DvadminSystemUserEmail.objects.all()[start_index:end_index]
        # 批量修改记录的状态
        for record in records_to_enable:
            print(f'Record ID: {record.id}, is_active: {record.is_active}')
            record.is_active = 0  # 假设修改状态字段为 is_active
            record.save()
        return DetailResponse(msg="修改成功")

    def process_email_account_wrapper(self, email_account,lock):
        print("线程"+email_account.username+"启动成功")
        self.process_email_account(email_account,lock)

    @action(methods=["POST"], detail=False)
    def selected_operation(self, request):
        import threading
        from concurrent.futures import ThreadPoolExecutor
        # todo  在这里获取 从数据库中获取启动状态的用户
        executeoperation = int(request.query_params.get('executeoperation'))
        # 选择谷歌登录
        if executeoperation == 1:
            try:
                lock = threading.Lock()
                email_accounts = DvadminSystemUserEmail.objects.all().filter(is_active=1, account_state=1)
                num_threads = len(email_accounts) *2
                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    [executor.submit(self.process_email_account_wrapper, email_account,lock) for email_account in
                     email_accounts]
                    time.sleep(1)
                return DetailResponse(msg="修改成功")
            except Exception as e:
                # 处理异常并返回错误信息
                error_message = f"An error occurred: {e}"
                return DetailResponse(msg=error_message)
        return DetailResponse(msg="修改成功")

    def TkClickByGoogle(self, driver):
        driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div/div/div[2]/div[3]').click()
        google_auth_login = driver.window_handles[1]
        driver.switch_to.window(google_auth_login)
        driver.implicitly_wait(3)

    def TkLoginByInfo(self, driver):
        act = ActionChains(driver)
        act.move_to_element(driver.find_element(
            By.XPATH, '//*[@id="loginContainer"]/div/div/div[2]/div[1]')).click().perform()
        time.sleep(1)
        months = driver.find_elements(
            By.XPATH, '//*[@id="loginContainer"]/div/div/div[2]/div[1]/div[2]/div')
        act.move_to_element(random.choice(months)).click().perform()

        act.move_to_element(driver.find_element(
            By.XPATH, '//*[@id="loginContainer"]/div/div/div[2]/div[2]')).click().perform()
        time.sleep(1)
        days = driver.find_elements(
            By.XPATH, '//*[@id="loginContainer"]/div/div/div[2]/div[2]/div[2]/div')
        act.move_to_element(random.choice(days)).click().perform()

        act.move_to_element(driver.find_element(
            By.XPATH, '//*[@id="loginContainer"]/div/div/div[2]/div[3]')).click().perform()
        time.sleep(1)
        years = driver.find_elements(
            By.XPATH, '//*[@id="loginContainer"]/div/div/div[2]/div[3]/div[2]/div')
        legit_years = years[20:38]
        act.move_to_element(random.choice(legit_years)).click().perform()

        driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div[1]/div/button').click()



    def TkLoginFristByGoogle(self, driver, email_account):
        time.sleep(2)
        # 获取新窗口的URL
        driver.implicitly_wait(5)
        driver.find_element(By.ID, 'identifierId').send_keys(email_account.username)
        driver.find_element(By.ID, 'identifierNext').click()
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(email_account.password)
        driver.find_element(By.ID, 'passwordNext').click()
        verication_elements = driver.find_element(By.XPATH, '//*[@id="confirm"]').click()
        if verication_elements:
            driver.find_element(By.XPATH, '//*[@id="confirm"]').click()
        email_account.login_num += 1

    def wait_xpath(self, xpath_pattern, driver):
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        element = (By.XPATH, xpath_pattern)
        WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located(element))

    def is_exist(self, xpath_pattern, driver) -> bool:
        """
        driver.find_element(*locator)
        :param xpath_pattern:
        :return False or the Element:
        """
        try:
            self.wait_xpath(xpath_pattern, driver)
            return True
        except Exception as e:
            return False

    def TkLoginNoFristByGoogle(self, driver, old_current_url):
        print("多次登录")
        driver.implicitly_wait(2)
        driver.find_element(
            By.XPATH,
            '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div').click()
        time.sleep(3)
        tik_tok = driver.window_handles[0]
        driver.switch_to.window(tik_tok)

        vericaiton_state = self.deal_verication_pic(driver)  # 0 无验证  1  环形   2 图片拖动  3 图片相同元素验证
        if vericaiton_state != 0:
            print("登录成功")
            self.deal_the_img(vericaiton_state, driver)
            time.sleep(3)
            self.TkLoginByInfo(driver)
            generate_e = EmailNameGenerator()
            str_list = generate_e.__repr__()
            username = str_list[2]
            driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div[1]/form/div[2]/div[1]/input').send_keys(
                username)
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div[1]/form/button').click()

            return False
        new_current_url = driver.execute_script("return window.location.href;")
        print("旧页面" + old_current_url)
        print("当前页面" + new_current_url)
        if old_current_url != new_current_url:
            print("登录成功")
            time.sleep(1)
            self.TkLoginByInfo(driver)
            vericaiton_state = self.deal_verication_pic(driver)  # 0 无验证  1  环形   2 图片拖动  3 图片相同元素验证
            if vericaiton_state != 0:
                self.deal_the_img(vericaiton_state, driver)
                time.sleep(5)
                generate_e = EmailNameGenerator()
                str_list = generate_e.__repr__()
                username = str_list[2]
                driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div[1]/form/div[2]/div[1]/input').send_keys(
                    username)
                time.sleep(1)
                driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div[1]/form/button').click()
                return False
        else:
            print("登录失败 重新登录")

    def deal_verication_pic(self, driver):
        res = self.is_exist('.//div[@class="sc-jTzLTM kuTGKN"]/img[2]', driver)
        if res:
            return 1
        res = self.is_exist('.//div[contains(@class,"captcha_verify_img--wrapper")]/img[2]', driver)
        if res:
            return 2
        res = self.is_exist('.//img[@id="captcha-verify-image"]', driver)
        if res:
            return 3
        return 0

    def TikTokRegister(self, email_account,lock):
        from selenium.common.exceptions import WebDriverException
        print("Tk注册 : " + email_account.username)
        driver = chrome_setup(email_account,lock)
        print("创建浏览器成功:"+email_account.username)
        current_window = driver.current_window_handle
        all_windows = driver.window_handles
        # 关闭其他窗口，确保只有一个窗口处于打开状态
        for window in all_windows:
            if window != current_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(current_window)
        driver.get('https://www.google.com/')
        driver.implicitly_wait(10)
        driver.get('https://www.tiktok.com/signup')
        old_current_url = driver.execute_script("return window.location.href;")
        time.sleep(2)
        print('tk页面打开成功:'+ email_account.username)
        # 设置最大尝试次数
        max_attempts = 3
        attempts = 0
        while attempts < max_attempts:
            try:
                time.sleep(3)
                print("点击谷歌登录:"+ email_account.username)
                driver.implicitly_wait(3)
                self.TkClickByGoogle(driver)
                verication_elements = driver.find_elements(By.XPATH, '//*[@id="identifierId"]')
                # 判断元素是否存在
                if verication_elements:
                    self.TkLoginFristByGoogle(driver, email_account)
                    vericaiton_state = self.deal_verication_pic(driver)  # 0 无验证  1  环形   2 图片拖动  3 图片相同元素验证
                    if vericaiton_state != 0:
                        self.deal_the_img(vericaiton_state, driver)
                        time.sleep(2)
                        self.TkLoginByInfo(driver)
                        generate_e = EmailNameGenerator()
                        str_list = generate_e.__repr__()
                        username = str_list[2]
                        driver.find_element(By.XPATH,
                                            '//*[@id="loginContainer"]/div[1]/form/div[2]/div[1]/input').send_keys(
                            username)
                        time.sleep(1)
                        driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div[1]/form/button').click()
                        email_account.account_type = 5
                        email_account.save()
                        break
                else:
                    if self.TkLoginNoFristByGoogle(driver, old_current_url) == False:
                        email_account.account_type = 5
                        email_account.save()
                        break
            except (TimeoutException, WebDriverException, Exception) as e:
                attempts += 1
            finally:
                email_account.save()

    def loginTiktokByGoogle(self, email_account, driver):
        '''
        //*[@id="confirm"]
        '''
        from selenium.common.exceptions import WebDriverException
        try:
            print("进入了输入账户页面")
            driver.implicitly_wait(10)
            print("获取用户名密码成功 账号：{} 密码：{}".format(email_account.username, email_account.password))
            username_element = driver.find_element(By.ID, 'identifierId')
            print("获取登录框元素")
            username_element.send_keys(email_account.usename)
            print("输入密码")
            driver.find_element(By.ID, 'identifierNext').click()
            print("点击下一步")
            driver.implicitly_wait(5)
            password_element = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
            password_element.send_keys(email_account.password)
            driver.find_element(By.ID, 'passwordNext').click()
        except WebDriverException as e:
            print("输入账号失败" + email_account.username)
    def process_email_account(self, email_account,lock):
        bro_id = email_account.bro_id
        if not bro_id:
            print(email_account.username+'创建浏览器中。。。。')
            email_account = self.createBro(email_account,lock)
            print('启动注册')
            self.TikTokRegister(email_account,lock)
        else:
            print('已有记录，直接注册')
            self.TikTokRegister(email_account,lock)

    # 获取一个未分配的代理
    def get_unassigned_proxy(self, email_account):
        from django.db.models import Q
        return DvadminSystemTiktokProxyConfig.objects.filter(
            Q(id=email_account.proxy_id) | Q(account_isnull=0, is_active=1)
        ).first()

    def deal_the_img(self, vericaiton_type, driver):
        '''
        :param vericaiton_type:  1 双环  2 图片拖动  3  图片 同样元素
        :return:
        '''
        from proxy_config.utils.common import common_download_image
        from proxy_config.utils.verication.powerddddocr import ddddOcr_tk
        from proxy_config.utils.verication.rotate_captcha import tk_circle_discern
        # img 外部容器
        img_outer_container = None
        this_xpath_pattern = None  # 图片 二维码 pattern
        if vericaiton_type == 1:  # 外环
            this_xpath_pattern = './/div[@class="sc-jTzLTM kuTGKN"]'
            img_outer_container = driver.find_element(By.XPATH, this_xpath_pattern)
        elif vericaiton_type == 2:  # 图片
            this_xpath_pattern = './/div[contains(@class,"captcha_verify_img--wrapper")]'
            img_outer_container = driver.find_element(By.XPATH, this_xpath_pattern)
        elif vericaiton_type == 3:
            this_xpath_pattern = './/img[@id="captcha-verify-image"]'
            input('please deal the problem by hand,input waiting...')
            return
        # 外圈图片   背景图片
        outer_pic = img_outer_container.find_element(By.XPATH, './img[1]')
        outer_pic = outer_pic.get_attribute('src')
        common_download_image(outer_pic, 'outer.png')  # 下载图片
        # 内圈图片   目标小图片
        inner_pic = img_outer_container.find_element(By.XPATH, './img[2]')
        inner_pic = inner_pic.get_attribute('src')
        # 下载到本地
        common_download_image(inner_pic, 'inner.png')  # 下载图片
        print('have download the two picture')
        # 验证码本地识别
        distance = None  # 需要拖动的距离
        if vericaiton_type:
            angle = tk_circle_discern('inner.png', 'outer.png')
            distance = angle / 180 * (340 - 64)
        else:
            distance = ddddOcr_tk('inner.png', 'outer.png')
            distance = distance * 0.62
        this_track = [int(distance // 4), int(distance // 4), int(distance * 0.3), int(distance * 0.2) + 5,
                      -8]  # 模拟鼠标拖动的点移
        this_track.append(int(distance) - sum(this_track))
        self.hold_on_slide(this_track, driver)  # 拖动滑块 模拟移动
        self.judge_the_img_src_change(driver, this_xpath_pattern + '/img[2]/@src', inner_pic, vericaiton_type)

    def hold_on_slide(self, tracks, driver):
        from selenium import webdriver
        import time, random
        try:
            slider = driver.find_element(By.XPATH, './/div[contains(@class,"secsdk-captcha-drag-icon")]')
            # 鼠标点击并按住不松
            webdriver.ActionChains(driver).click_and_hold(slider).perform()
            # 让鼠标随机往下移动一段距离
            webdriver.ActionChains(driver).move_by_offset(xoffset=0, yoffset=100).perform()
            time.sleep(0.15)
            for item in tracks:
                webdriver.ActionChains(driver).move_by_offset(xoffset=item,
                                                              yoffset=random.randint(-1, 1)).perform()
                time.sleep(random.uniform(0.02, 0.15))
            # 稳定一秒再松开 //*[@id="loginContainer"]/div[1]/form/div[2]/div[1]/input
            time.sleep(1)
            webdriver.ActionChains(driver).release().perform()
            time.sleep(1)
        except Exception as e:
            print(e)

    def judge_the_img_src_change(self, driver, this_xpath_pattern, last_inner_img_url: str, circle):
        this_xpath_pattern = this_xpath_pattern  # inner_img_url pattern
        response = driver.page_source
        html = etree.HTML(response)
        verication = html.xpath('.//div[contains(@class,"captcha_verify_container")]')  # 验证码块
        import time
        if verication:
            img_src = html.xpath(this_xpath_pattern)  # 验证码图片
            if len(img_src) == 1 and img_src[0] != last_inner_img_url:  # 验证码已经改变
                # self.browser.implicitly_wait(5)
                print("img_src%s" % img_src)
                time.sleep(5)  # 等待 5s
                self.deal_the_img(circle, driver)
            # 验证码没有改变 或者加载错误
            else:
                time.sleep(5)
                self.judge_the_img_src_change(driver, this_xpath_pattern, last_inner_img_url, circle)
        else:
            print('Success to over the picture')
            self.verication_success = True  # 成功
            return True

    def createBro(self, email_account,lock):
        import requests
        port = generate_port()
        # 筛选is_active字段为1的用户邮箱信息
        proxy = self.get_unassigned_proxy(email_account)
        print(email_account.username+"获取代理成功")
        print(proxy)
        url = "http://local.adspower.net:50325/api/v1/user/create"
        # 如果存在is_active字段为1的用户邮箱信息
        if proxy:
            # 创建并保存到dvadmin_system_tiktok_proxy_config表
            # 构建用户代理配置
            payload = {
                "name": "test",
                "group_id": "0",
                "repeat_config": [
                    "0"
                ],
                "fingerprint_config": {
                    "flash": "block",
                    "scan_port_type": "1",
                    "screen_resolution": "1024_768",
                    "fonts": [
                        "all"
                    ],
                    "longitude": "180",
                    "latitude": "90",
                    "webrtc": "proxy",
                    "do_not_track": "true",
                    "hardware_concurrency": "default",
                    "device_memory": "default"
                }
                ,
                "user_proxy_config": {
                    "proxy_soft": "other",
                    "proxy_type": "socks5",
                    "proxy_host": proxy.IP,
                    "proxy_port": proxy.port,
                    "proxy_user": proxy.username,
                    "proxy_password": proxy.password,
                }
            }
            headers = {
                'Content-Type': 'application/json'
            }
            try:
                print(proxy.username)
                with lock:
                    response = requests.request("POST", url, headers=headers, json=payload).json()
                print(response)
                text = response
                print(email_account.username+"创建浏览器成功")
                # 如果没有这个浏览器 则进行另外一个操作
                new_browser_id = text['data']['id']
                # 假设email_account是一个DvadminSystemUserEmail对象
                email_account.bro_id = new_browser_id
                email_account.proxy_id = proxy.id
                proxy.browser_id = new_browser_id
                proxy.local_port = port
                proxy.account_isnull = 1
                proxy.save()
            except Exception as e:
                print(f"请查看ads浏览器连接是否正常，请查看" + {e})
                # 等待一段时间后进行重试
                time.sleep(1)
            return email_account
