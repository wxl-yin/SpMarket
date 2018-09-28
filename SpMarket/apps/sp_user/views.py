import uuid

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from db.base_view import BaseVerifyView
from sp_user.forms import RegisterForm, LoginForm
from sp_user.helper import verify_login_required, send_sms
from sp_user.models import Users


class RegisterView(View):
    # 注册功能
    def get(self, request):
        # 使用form渲染页面
        form = RegisterForm()
        return render(request, "sp_user/reg.html", {"form": form})

    def post(self, request):
        # 1. 接收数据
        session_code = request.session.get('random_code')
        # 强制转换成真正的字典
        data = request.POST.dict()
        data['session_code'] = session_code
        # 2. 处理数据
        form = RegisterForm(data)
        # 3. 响应
        if form.is_valid():
            form.save()
            # 注册成功,跳转到登录页面
            return redirect(reverse("sp_user:login"))

        # 注册失败,回到注册页面,提示错误信息
        return render(request, "sp_user/reg.html", {"form": form})


class LoginView(View):
    # 登录功能
    def get(self, request):
        login_form = LoginForm()
        return render(request, "sp_user/login.html", {"form": login_form})

    def post(self, request):
        # 接收数据
        # 处理数据
        login_form = LoginForm(request.POST)
        # 响应
        if login_form.is_valid():
            # 验证成功,保存登录标识到session
            user = login_form.cleaned_data.get("user")
            request.session['ID'] = user.pk
            request.session['phone'] = user.phone
            # 设置有效期, 关闭浏览器就 重新登录
            request.session.set_expiry(0)

            # 跳转到用户中心
            # 有办法获取到跳转的位置, 没有必要跳转到个人中心
            if request.GET.get('next', None):
                return redirect(request.GET.get('next'))
            return redirect(reverse('sp_user:center'))
        # 验证失败
        return render(request, "sp_user/login.html", {"form": login_form})


class CenterView(BaseVerifyView):
    # 个人中心功能
    def get(self, request):
        phone = request.session.get('phone')
        context = {
            "phone": phone
        }
        return render(request, "sp_user/member.html", context)

    def post(self, request):
        pass


class AddressView(BaseVerifyView):
    # 收货地址功能
    def get(self, request):
        pass

    def post(self, request):
        pass


class InfoView(BaseVerifyView):
    # 个人资料功能
    def get(self, request):
        # 验证用户是否登录
        user_id = request.session.get("ID")
        # 查询当前用户的所有信息
        user = Users.objects.filter(pk=user_id).first()

        context = {
            "user": user
        }
        return render(request, "sp_user/infor.html", context)

    def post(self, request):
        # 1. 接收数据
        user_id = request.session.get("ID")
        data = request.POST
        file = request.FILES['head']
        # 2. 处理数据
        # 更新用户的头像
        user = Users.objects.get(pk=user_id)
        user.head = file
        user.save()
        # 3. 响应
        return redirect(reverse("sp_user:center"))


# 单独使用一个视图函数处理图片的上传
@csrf_exempt  # 移除令牌限制
def upload_head(request):
    if request.method == "POST":
        # 获取用户的id
        user_id = request.session.get("ID")
        # 获取用户对象
        user = Users.objects.get(pk=user_id)
        # 保存图片
        user.head = request.FILES['file']  # 通过键获取对应的文件
        user.save()
        return JsonResponse({"error": 0})
    else:
        return JsonResponse({"error": 1})

    # # 登录验证的装饰器
    # @method_decorator(verify_login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


# 登录验证装饰器的使用 函数形式
@verify_login_required
def info(request):
    return render(request, "sp_user/infor.html")


class LogoutView(View):
    # 退出功能
    def get(self, request):
        pass

    def post(self, request):
        pass


class SendCodeView(View):
    """
        发送验证码
    """

    def post(self, request):
        # 1. 接收请求数据
        phone = request.POST.get("tel", "")
        # 2. 处理数据
        # 手机号码格式判断 正则判断
        import re
        # 设置验证的正则规则
        phone_re = re.compile("^1[3-9]\d{9}$")
        # 匹配 手机号字符串
        res = re.search(phone_re, phone)
        if res is None:
            # 手机号码格式错误
            return JsonResponse({"status": "400", "msg": "手机号码格式错误"})

        # 该手机号是否已经注册
        res = Users.objects.filter(phone=phone).exists()
        if res:
            # 手机号码格式错误
            return JsonResponse({"status": "400", "msg": "手机号码已经注册"})

        # 生成随机验证码这个数字
        import random
        random_code = "".join([str(random.randint(0, 9)) for _ in range(4)])
        # print(random_code)

        # 发送验证码 使用阿里云发送, 开发自己模拟
        print("===========code==={}==================".format(random_code))
        __business_id = uuid.uuid1()
        # print(__business_id)
        params = "{\"code\":\"%s\"}" % random_code
        rs = send_sms(__business_id, phone, "尹强", "SMS_141905190", params)
        print(rs)

        # ? 将生成的随机码保存到session中
        request.session['random_code'] = random_code
        request.session.set_expiry(60)

        # 3. 响应 json , 告知 ajax是否发送成功
        return JsonResponse({"status": "200"})
