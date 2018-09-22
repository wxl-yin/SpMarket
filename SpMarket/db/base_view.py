from django.utils.decorators import method_decorator
from django.views import View

from sp_user.helper import verify_login_required


class BaseVerifyView(View):
    """
        基础视图类, 不是所有的视图类都可以继承该视图,
        只有需要验证的视图类 才继承
    """
    # 登录验证的装饰器
    @method_decorator(verify_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)