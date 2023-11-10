# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class CaptchaCaptchastore(models.Model):
    challenge = models.CharField(max_length=32)
    response = models.CharField(max_length=32)
    hashkey = models.CharField(unique=True, max_length=40)
    expiration = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'captcha_captchastore'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DvadminAccountData(models.Model):
    id = models.IntegerField(primary_key=True)
    decsp = models.CharField(max_length=255, blank=True, null=True)
    accout = models.CharField(max_length=255, blank=True, null=True)
    fans_count = models.IntegerField(blank=True, null=True)
    video_count = models.IntegerField(blank=True, null=True)
    proxy_address = models.CharField(max_length=255, blank=True, null=True)
    material_path = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    account_state = models.IntegerField(blank=True, null=True)
    account_type = models.IntegerField(blank=True, null=True)
    descp = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_account_data'


class DvadminApiWhiteList(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    url = models.CharField(max_length=200)
    method = models.IntegerField(blank=True, null=True)
    enable_datasource = models.IntegerField()
    creator_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_api_white_list'


class DvadminMessageCenter(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    target_type = models.IntegerField()
    creator_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_message_center'


class DvadminMessageCenterTargetDept(models.Model):
    messagecenter_id = models.BigIntegerField()
    dept_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'dvadmin_message_center_target_dept'
        unique_together = (('messagecenter_id', 'dept_id'),)


class DvadminMessageCenterTargetRole(models.Model):
    messagecenter_id = models.BigIntegerField()
    role_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'dvadmin_message_center_target_role'
        unique_together = (('messagecenter_id', 'role_id'),)


class DvadminMessageCenterTargetUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)
    creator_id = models.BigIntegerField(blank=True, null=True)
    messagecenter_id = models.BigIntegerField()
    users_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'dvadmin_message_center_target_user'


class DvadminSystemArea(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=100)
    code = models.CharField(unique=True, max_length=20)
    level = models.BigIntegerField()
    pinyin = models.CharField(max_length=255)
    initials = models.CharField(max_length=20)
    enable = models.IntegerField()
    creator_id = models.BigIntegerField(blank=True, null=True)
    pcode_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_area'


class DvadminSystemConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=50)
    key = models.CharField(max_length=200)
    value = models.JSONField(blank=True, null=True)
    sort = models.IntegerField()
    status = models.IntegerField()
    data_options = models.JSONField(blank=True, null=True)
    form_item_type = models.IntegerField()
    rule = models.JSONField(blank=True, null=True)
    placeholder = models.CharField(max_length=100, blank=True, null=True)
    setting = models.JSONField(blank=True, null=True)
    creator_id = models.BigIntegerField(blank=True, null=True)
    parent_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_config'
        unique_together = (('key', 'parent_id'),)


class DvadminSystemDept(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=64)
    key = models.CharField(unique=True, max_length=64, blank=True, null=True)
    sort = models.IntegerField()
    owner = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=32, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    creator_id = models.BigIntegerField(blank=True, null=True)
    parent_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_dept'


class DvadminSystemDictionary(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    value = models.CharField(max_length=200, blank=True, null=True)
    type = models.IntegerField()
    color = models.CharField(max_length=20, blank=True, null=True)
    is_value = models.IntegerField()
    status = models.IntegerField()
    sort = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=2000, blank=True, null=True)
    creator_id = models.BigIntegerField(blank=True, null=True)
    parent_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_dictionary'


class DvadminSystemFileList(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    file_url = models.CharField(max_length=255)
    engine = models.CharField(max_length=100)
    mime_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    md5sum = models.CharField(max_length=36)
    creator_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_file_list'


class DvadminSystemLoginLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    ip = models.CharField(max_length=32, blank=True, null=True)
    agent = models.TextField(blank=True, null=True)
    browser = models.CharField(max_length=200, blank=True, null=True)
    os = models.CharField(max_length=200, blank=True, null=True)
    continent = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    isp = models.CharField(max_length=50, blank=True, null=True)
    area_code = models.CharField(max_length=50, blank=True, null=True)
    country_english = models.CharField(max_length=50, blank=True, null=True)
    country_code = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    login_type = models.IntegerField()
    creator_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_login_log'


class DvadminSystemMenu(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    icon = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=64)
    sort = models.IntegerField(blank=True, null=True)
    is_link = models.IntegerField()
    is_catalog = models.IntegerField()
    web_path = models.CharField(max_length=128, blank=True, null=True)
    component = models.CharField(max_length=128, blank=True, null=True)
    component_name = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField()
    frame_out = models.IntegerField()
    cache = models.IntegerField()
    visible = models.IntegerField()
    creator_id = models.BigIntegerField(blank=True, null=True)
    parent_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_menu'


class DvadminSystemMenuButton(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=64)
    api = models.CharField(max_length=200)
    method = models.IntegerField(blank=True, null=True)
    creator_id = models.BigIntegerField(blank=True, null=True)
    menu_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'dvadmin_system_menu_button'


class DvadminSystemOperationLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    request_modular = models.CharField(max_length=64, blank=True, null=True)
    request_path = models.CharField(max_length=400, blank=True, null=True)
    request_body = models.TextField(blank=True, null=True)
    request_method = models.CharField(max_length=8, blank=True, null=True)
    request_msg = models.TextField(blank=True, null=True)
    request_ip = models.CharField(max_length=32, blank=True, null=True)
    request_browser = models.CharField(max_length=64, blank=True, null=True)
    response_code = models.CharField(max_length=32, blank=True, null=True)
    request_os = models.CharField(max_length=64, blank=True, null=True)
    json_result = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    creator_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_operation_log'


class DvadminSystemPost(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=32)
    sort = models.IntegerField()
    status = models.IntegerField()
    creator_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_post'


class DvadminSystemRole(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=64)
    key = models.CharField(unique=True, max_length=64)
    sort = models.IntegerField()
    status = models.IntegerField()
    admin = models.IntegerField()
    data_range = models.IntegerField()
    remark = models.TextField(blank=True, null=True)
    creator_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_role'


class DvadminSystemRoleDept(models.Model):
    role_id = models.BigIntegerField()
    dept_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'dvadmin_system_role_dept'
        unique_together = (('role_id', 'dept_id'),)


class DvadminSystemRoleMenu(models.Model):
    role_id = models.BigIntegerField()
    menu_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'dvadmin_system_role_menu'
        unique_together = (('role_id', 'menu_id'),)


class DvadminSystemRolePermission(models.Model):
    role_id = models.BigIntegerField()
    menubutton_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'dvadmin_system_role_permission'
        unique_together = (('role_id', 'menubutton_id'),)

from dvadmin.utils.models import CoreModel, table_prefix

class DvadminSystemTiktokProxyConfig(CoreModel):
    id = models.AutoField(unique=True, primary_key=True, db_index=True, verbose_name="代理id")
    username = models.CharField(max_length=200, unique=True, verbose_name="username")
    password = models.CharField(max_length=100, verbose_name="password")
    IP = models.CharField(max_length=100, verbose_name="IP地址")
    PROXY_TYPE = (
        (0, "socks5"),
        (1, "http"),
    )
    type = models.IntegerField(choices=PROXY_TYPE, verbose_name="type代理类型")
    port = models.CharField(max_length=100, default=4600, verbose_name="port ip端口")
    local_port = models.CharField(max_length=100, null=True, verbose_name="本地port ip端口")
    local_proxy_port_traffic = models.CharField(max_length=100, null=True, default=0,
                                                verbose_name="本地代理端口流量统计")
    STATUS_CHOICES = (
        (0, "禁用"),
        (1, "启用"),
    )
    is_active = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="状态")

    class Meta:
        db_table = table_prefix + "system_tiktok_proxy_config"
        verbose_name = '代理配置表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class Meta:
        managed = False
        db_table = 'dvadmin_system_tiktok_proxy_config'


class DvadminSystemUserEmail(models.Model):
    desc_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    fans_count = models.BigIntegerField(blank=True, null=True)
    video_count = models.BigIntegerField(blank=True, null=True)
    proxy_address = models.CharField(max_length=150, blank=True, null=True)
    mari_dir = models.CharField(max_length=100, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    account_type = models.IntegerField(blank=True, null=True)
    account_state = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    pri_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_user_email'


class DvadminSystemUsers(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    modifier = models.CharField(max_length=255, blank=True, null=True)
    dept_belong_id = models.CharField(max_length=255, blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    username = models.CharField(unique=True, max_length=150)
    employee_no = models.CharField(unique=True, max_length=150, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=40)
    gender = models.IntegerField(blank=True, null=True)
    user_type = models.IntegerField(blank=True, null=True)
    last_token = models.CharField(max_length=255, blank=True, null=True)
    creator_id = models.BigIntegerField(blank=True, null=True)
    dept_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_users'

class DvadminSystemUsersGroups(models.Model):
    users = models.ForeignKey(DvadminSystemUsers, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_users_groups'
        unique_together = (('users', 'group'),)


class DvadminSystemUsersPost(models.Model):
    users_id = models.BigIntegerField()
    post_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'dvadmin_system_users_post'
        unique_together = (('users_id', 'post_id'),)


class DvadminSystemUsersRole(models.Model):
    users_id = models.BigIntegerField()
    role_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'dvadmin_system_users_role'
        unique_together = (('users_id', 'role_id'),)


class DvadminSystemUsersUserPermissions(models.Model):
    users = models.ForeignKey(DvadminSystemUsers, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dvadmin_system_users_user_permissions'
        unique_together = (('users', 'permission'),)


class TokenBlacklistBlacklistedtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(DvadminSystemUsers, models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'
