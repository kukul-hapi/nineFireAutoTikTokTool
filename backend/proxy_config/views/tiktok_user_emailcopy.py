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
        driver = chrome_setup(email_account)  # Setting up the ChromeDriver
        current_window = driver.current_window_handle
        all_windows = driver.window_handles
        print(vars(email_account))
        # 关闭其他窗口，确保只有一个窗口处于打开状态
        for window in all_windows:
            if window != current_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(current_window)
        driver.get('https://www.google.com/')
        driver.implicitly_wait(10)
        driver.get('https://www.tiktok.com/signup')
        print('tk页面打开成功')
        driver.implicitly_wait(3)
        # 设置最大尝试次数
        max_attempts = 3
        attempts = 0
        enterAccount = False
        # 扫描页面 如果出现了账号密码输入框。。。。
        while attempts < max_attempts:
            try:
                # 选择谷歌登录
                driver.find_element(
                    By.XPATH, '//*[@id="loginContainer"]/div/div/div[2]/div[3]').click()
                print('谷歌登录页面打开成功')
                driver.implicitly_wait(5)
                # 获取所有窗口句柄、
                google_auth_login = driver.window_handles[1]
                driver.switch_to.window(google_auth_login)
                find_element = driver.find_element(By.ID, 'identifierId')
                driver.implicitly_wait(5)
                username = email_account.username
                password = email_account.password
                print("获取用户名密码成功 账号：" + {username} + +"密码：" + {password})
                # 如果 'identifierId' 元素出现，运行登录操作 输入账号密码 。。。
                enterAccount = self.loginTiktokByGoogle(username, password, driver, enterAccount)
                if enterAccount:
                    break
                attempts += 1
                print(attempts)
            except NoSuchElementException as e:
                # 如果 'identifierId' 元素不存在，不执行登录操作
                try:
                    driver.implicitly_wait(10)
                    element = driver.find_element(By.XPATH,'//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]')
                    element.click()
                    attempts += 1
                    print(f"没找到登录框: {e}")
                except NoSuchElementException:
                    print("两个元素都未找到")
                    attempts += 1
                    print(attempts)
                else:
                    print("找到第二个元素")
            else:
                print("找到第一个元素")

    def loginTiktokByGoogle(self, usename, password, driver, enterAccount):
        try:
            print("进入了输入账户页面")
            driver.implicitly_wait(10)
            driver.find_element(By.ID, 'identifierId').send_keys(usename)
            driver.find_element(By.ID, 'identifierNext').click()
            driver.implicitly_wait(3)
            driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
            driver.find_element(By.ID, 'passwordNext').click()

            return enterAccount
        except:
            pass
    def process_email_account(self, email_account):
        bro_id = email_account.bro_id
        if not bro_id:
            email_account = self.createBro(email_account)
            self.TikTokRegister(email_account)
        else:
            self.TikTokRegister(email_account)

    # 获取一个未分配的代理
    def get_unassigned_proxy(self):
        return DvadminSystemTiktokProxyConfig.objects.filter(account_isnull=0, is_active=1).first()

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
                response = requests.request("POST", url, headers=headers, json=payload)
                text = response.json()
                # 如果没有这个浏览器 则进行另外一个操作
                new_browser_id = text['data']['id']
                # 假设email_account是一个DvadminSystemUserEmail对象
                email_account.bro_id = new_browser_id
                email_account.proxy_id = proxy.id
                proxy.browser_id = new_browser_id
                proxy.local_port = port
                print("进入注册1111111111111")
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
        print(executeoperation)
        # 选择谷歌登录
        if executeoperation == 1:
            try:
                email_accounts = DvadminSystemUserEmail.objects.all().filter(is_active=1)
                # 创建一个 Lock，用于确保线程安全
                lock = threading.Lock()
                # 设置线程数量为 email_accounts 的数量
                num_threads = len(email_accounts)
                print(num_threads)
                # 使用 ThreadPoolExecutor 创建一个线程池
                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    # 使用 submit 提交每个邮箱账户的处理任务
                    for email_account in email_accounts:
                        executor.submit(self.process_email_account_wrapper, email_account, lock)

            except Exception as e:
                # 处理异常并返回错误信息
                error_message = f"An error occurred: {e}"
                return DetailResponse(msg=error_message)
        return DetailResponse(msg="修改成功")
