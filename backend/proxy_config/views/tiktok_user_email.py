# Create your views here.
from proxy_config.models import DvadminSystemUserEmail
from proxy_config.utils.serializers import TKUserEmailModelSerializer,TKUserEmailModelCreateUpdateSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from rest_framework import serializers
# from backend.proxy_config.models import TiktokProxyConfig
from rest_framework.decorators import action, permission_classes
from dvadmin.utils.json_response import ErrorResponse, DetailResponse

from proxy_config.browser.chrome import chrome_setup
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
    filter_fields = ['desc_name', 'username', 'fans_count', 'video_count', 'proxy_address', 'mari_dir', 'update_datetime',
                     'is_active','account_type','description','account_state']
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

        print(start_index,end_index)
        # 获取要批量修改的记录
        records_to_enable = DvadminSystemUserEmail.objects.all()[start_index:end_index]
        # 批量修改记录的状态
        for record in records_to_enable:
            print(f'Record ID: {record.id}, is_active: {record.is_active}')
            record.is_active = 1  # 假设修改状态字段为 is_active
            record.save()

        return DetailResponse(msg="修改成功")

    def TikTokRegister(self,country, ads_id):
        from selenium.common.exceptions import NoSuchElementException, WebDriverException
        driver = chrome_setup(ads_id)  # Setting up the ChromeDriver
        # browserId = createBrowser()
        shadow = Shadow(driver)  # Declaring the shadow module
        # Declaring the mouse and keyboard actions module
        act = ActionChains(driver)
        # db = DB()
        #########################

        driver.get('https://www.google.com/')
        time.sleep(3)
        driver.get('https://www.tiktok.com/signup')
        print('The Tik-Tok page reached!')
        driver.implicitly_wait(3)

        driver.find_element(
            By.XPATH, '//*[@id="loginContainer"]/div/div/div[2]/div[3]').click()
        time.sleep(5)

        # Accept cookies shadowDOM function
        try:
            driver.implicitly_wait(200)
            shadow_root = driver.find_element(By.XPATH, '//tiktok-cookie-banner')
            button = shadow.find_element(
                shadow_root, 'div > div.button-wrapper > button:nth-child(2)')
            act.move_to_element(button).click(button).perform()
            print('Cookies dismissed!')
            time.sleep(3)
        except Exception as E:
            print(f'Cookies issue:{E}')

        # 获取所有窗口句柄
        tik_tok = driver.window_handles[0]
        google_auth_login = driver.window_handles[1]

        driver.switch_to.window(google_auth_login)
        driver.implicitly_wait(10)
        username = 'XL9YYqlDkHi1@yooutu.vip'
        password = '05Byxlnh4vhe'
        enterAccount = True
        # 扫描页面 如果出现了账号密码输入框。。。。
        while enterAccount:
            try:
                print("identifierId")
                element = driver.find_element(By.ID, 'identifierId')
                # 如果 'identifierId' 元素出现，运行登录操作 输入账号密码 。。。
                enterAccount = self.loginTiktokByGoogle(username, password, driver, enterAccount)
                print("出来了。。。")
                if enterAccount == False:
                    print("11111")
                    driver.implicitly_wait(10)
                    element = driver.find_element(By.XPATH,
                                                  '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]')
                    element.click()
                    driver.window_handles
                    enterAccount = True
                    # 如果 'element' 元素出现，进行点击登录操作

            except NoSuchElementException:
                # 如果 'identifierId' 元素不存在，不执行登录操作
                pass

    def loginTiktokByGoogle(self,usename, password, driver, enterAccount):
        try:
            print("进入了输入账户页面")
            driver.implicitly_wait(10)
            # 输入账号密码
            print("进入了输入账号")
            driver.find_element(By.ID, 'identifierId').send_keys(usename)
            driver.find_element(By.ID, 'identifierNext').click()
            driver.implicitly_wait(3)
            print("进入了输入密码")
            driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
            driver.find_element(By.ID, 'passwordNext').click()
            print("再次登录 当前页面为" + driver.window_handles)
            return enterAccount
        except:
            pass

    def createBro(self):
        import requests
        url = "http://local.adspower.net:50325/api/v1/user/create"
        payload = {
            "name": "test",
            "group_id": "0",
            "repeat_config": [
                "0"
            ],
            "fingerprint_config": {
                "flash": "block",
                "scan_port_type": "1",
                "screen_resolution": "1920_1080",
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
                "proxy_host": "78f609233452dcb5.as.roxlabs.vip",
                "proxy_port": "4600",
                "proxy_user": "user-lxy654321-region-sg-sessid-sg2jP09d7J-sesstime-1-keep-true",
                "proxy_password": "111222"
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        text = response.json()
        print(text)
        ads_id = text['data']['id']
        return ads_id

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

    @action(methods=["POST"], detail=False)
    def selected_operation(self, request):
        executeoperation = int(request.query_params.get('executeoperation'))
        if executeoperation == 1:
            # 在这里需要获取一些激活id的 也就是
            ads_id =  self.createBro()
            self.TikTokRegister("aaaa",ads_id)
            print(ads_id)
            pass
        return DetailResponse(msg="修改成功")