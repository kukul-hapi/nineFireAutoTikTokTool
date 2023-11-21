# Create your views here.
from proxy_config.models import DvadminSystemUserEmail, DvadminSystemTiktokProxyConfig
from proxy_config.utils.serializers import TKUserEmailModelSerializer, TKUserEmailModelCreateUpdateSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from rest_framework import serializers
# from backend.proxy_config.models import TiktokProxyConfig
from rest_framework.decorators import action, permission_classes
from dvadmin.utils.json_response import ErrorResponse, DetailResponse

from proxy_config.browser.chrome import chrome_setup, generate_port
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from password_generator import PasswordGenerator
from pyshadow.main import Shadow
import time
import random
import re


class ExportUserProfileSerializer(CustomModelSerializer):
    #     """
    #     tiktol配置导出 序列化器
    #     """
    pass


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
    export_serializer_class = ExportUserProfileSerializer

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

    def TikTokRegister(self, email_account):
        from selenium.common.exceptions import NoSuchElementException, WebDriverException
        print("Tk注册")
        driver = chrome_setup(email_account)
        # 创建浏览器成功
        print("创建浏览器成功")
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
        driver.implicitly_wait(3)
        print('tk页面打开成功')
        # 设置最大尝试次数
        max_attempts = 3
        attempts = 0
        enterAccount = False
        while attempts < max_attempts:
            # 选择谷歌登录
            time.sleep(5)
            driver.find_element(
                By.XPATH, '//*[@id="loginContainer"]/div/div/div[2]/div[3]').click()
            time.sleep(5)
            print('谷歌登录页面打开成功')
            # 获取所有窗口句柄、
            tik_tok = driver.window_handles[0]
            old_current_url = driver.execute_script("return window.location.href;")
            print(f"Current URL: {old_current_url}")
            google_auth_login = driver.window_handles[1]
            driver.switch_to.window(google_auth_login)
            # 获取新窗口的URL
            new_window_url = driver.current_url
            # 打印URL或进行其他操作
            print(f"URL of the new window: {new_window_url}")
            if attempts >= 1 or email_account.login_num > 0:
                print("多次登录")
                driver.implicitly_wait(10)
                driver.find_element(
                    By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div').click()
                time.sleep(10)
                driver.switch_to.window(tik_tok)
                new_current_url = driver.execute_script("return window.location.href;")
                print(f"Current URL: {new_current_url}")
                if old_current_url != new_current_url:
                    print("登录成功")
                else:
                    print("登录失败")
            elif  attempts == 0 or email_account.login_num == 0:
                print("首次登录")
                print("attempts:" + attempts + "login_num:" + email_account.login_num)
                driver.implicitly_wait(10)
                driver.find_element(By.ID, 'identifierId'). send_keys("fasfsaef@gmail.com")
                driver.find_element(By.ID, 'identifierNext').click()
                print("点击下一步")
                driver.implicitly_wait(3)
                driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys('bYh9Akg!5')
                driver.find_element(By.ID, 'passwordNext').click()
                email_account.login_num+=1
            # 如果 'identifierId' 元素出现，运行登录操作 输入账号密码 。。。
            # enterAccount = self.loginTiktokByGoogle(email_account, driver, enterAccount)
            attempts += 1
            print("attempts : "+attempts)


    def loginTiktokByGoogle(self, email_account, driver, enterAccount):
        from selenium.common.exceptions import NoSuchElementException, WebDriverException
        try:
            print("进入了输入账户页面")
            driver.implicitly_wait(10)
            print("获取用户名密码成功 账号：{} 密码：{}".format(email_account.username, email_account.password))
            username_element =driver.find_element(By.ID, 'identifierId')
            print("获取登录框元素")
            username_element.send_keys(email_account.usename)
            print("输入密码")
            driver.find_element(By.ID, 'identifierNext').click()
            print("点击下一步")
            driver.implicitly_wait(3)
            password_element = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
            password_element.send_keys(email_account.password)
            driver.find_element(By.ID, 'passwordNext').click()



        except WebDriverException as e :
            print("输入账号失败"+e)
            pass

    def process_email_account(self, email_account):
        bro_id = email_account.bro_id
        if not bro_id:
            print('创建浏览器')
            email_account = self.createBro(email_account)
            self.TikTokRegister(email_account)
        else:
            print('wei创建浏览器')
            self.TikTokRegister(email_account)

    # 获取一个未分配的代理
    def get_unassigned_proxy(self):
        return DvadminSystemTiktokProxyConfig.objects.filter(account_isnull=0, is_active=1).first()

    def deal_the_img(self, vericaiton_type):
        '''
        :param vericaiton_type:  1 双环    2 图片拖动 3  图片 同样元素
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
            img_outer_container = self.browser.find_element(By.XPATH, this_xpath_pattern)
        elif vericaiton_type == 2:  # 图片
            this_xpath_pattern = './/div[contains(@class,"captcha_verify_img--wrapper")]'
            img_outer_container = self.browser.find_element(By.XPATH, this_xpath_pattern)
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
        self.hold_on_slide(this_track)  # 拖动滑块 模拟移动
        self.judge_the_img_src_change(this_xpath_pattern + '/img[2]/@src', inner_pic, vericaiton_type)
    def createBro(self, email_account):
        import requests
        port = generate_port()
        # 筛选is_active字段为1的用户邮箱信息
        proxy = self.get_unassigned_proxy()
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
                print("创建新的浏览器")
                response = requests.request("POST", url, headers=headers, json=payload)
                text = response.json()

                # 如果没有这个浏览器 则进行另外一个操作
                new_browser_id = text['data']['id']
                # 假设email_account是一个DvadminSystemUserEmail对象
                email_account.bro_id = new_browser_id
                email_account.proxy_id = proxy.id
                proxy.browser_id = new_browser_id
                proxy.local_port = port
                proxy.account_isnull = 1
                proxy.save()
                email_account.save()
            except requests.exceptions.RequestException as e:
                print(f"请查看ads浏览器连接是否正常，请查看" + {e})
                # 等待一段时间后进行重试
                time.sleep(1)
            return email_account

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

    def process_email_account_wrapper(self,email_account,lock):
        # 在这里调用你的 process_email_account 函数
        # 确保这个函数是线程安全的
        # 例如，可以使用 Lock 来确保线程安全
        lock.acquire()
        try:
            self.process_email_account(email_account)
        finally:
            lock.release()

    @action(methods=["POST"], detail=False)
    def selected_operation(self, request):
        import threading
        from concurrent.futures import ThreadPoolExecutor
        '''
        此处 获取激活账户 然后获取激活ip 然后查看账户中是否有填写 如果没有则进行创建填写 分配 如果
        '''
        # todo  在这里获取 从数据库中获取启动状态的用户
        executeoperation = int(request.query_params.get('executeoperation'))
        # 选择谷歌登录
        if executeoperation == 1:
            try:
                email_accounts = DvadminSystemUserEmail.objects.all().filter(is_active=1)
                # 创建一个 Lock，用于确保线程安全
                lock = threading.Lock()
                # 设置线程数量为 email_accounts 的数量
                num_threads = len(email_accounts)*4
                # 使用 ThreadPoolExecutor 创建一个线程池
                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    # 使用 submit 提交每个邮箱账户的处理任务
                    for email_account in email_accounts:
                        print(email_account)
                        executor.submit(self.process_email_account_wrapper, email_account, lock)

            except Exception as e:
                # 处理异常并返回错误信息
                error_message = f"An error occurred: {e}"
                return DetailResponse(msg=error_message)
        return DetailResponse(msg="修改成功")
