import hashlib
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
# from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
# import uuid
from aliyunsdkcore.profile import region_provider
# from aliyunsdkcore.http import method_type as MT
# from aliyunsdkcore.http import format_type as FT
from django.conf import settings

# 设置密码的加密
from django.shortcuts import redirect
from django.urls import reverse


def set_password(pwd):
    token = settings.SECRET_KEY
    password = token + pwd
    h = hashlib.sha1(password.encode("utf-8"))
    return h.hexdigest()


# 登录验证装饰器, 用于验证是否登录
def verify_login_required(func):
    """
    :param func:  旧函数
    :return:
    """
    # 定义一个新函数
    def verify_login(request, *args, **kwargs):
        if request.session.get("ID") is None:
            # 没有登录
            return redirect(reverse("sp_user:login"))
        else:
            return func(request, *args, **kwargs)

    # 返回新函数
    return verify_login


# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse

