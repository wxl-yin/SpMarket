from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from sp_goods.models import GoodsSKU


class IndexView(View):
    # 首页
    def get(self, request):
        return render(request, "sp_goods/index.html")

    def post(self, request):
        pass


class CategoryView(View):
    # 列表页
    def get(self, request):
        # sku商品
        goods_skus = GoodsSKU.objects.filter(is_delete=False)

        # 组装一个字典
        context = {
            "goods_skus": goods_skus
        }
        return render(request, "sp_goods/category.html", context)

    def post(self, request):
        pass


class DetailView(View):
    # 详情页
    def get(self, request, sku_id):
        try:
            # 接收
            sku_id = int(sku_id)
            # 处理
            goods_sku = GoodsSKU.objects.get(pk=sku_id)

            # gallers = goods_sku.gallery_set.all()
            # 响应
            context = {
                "goods_sku": goods_sku
            }
            return render(request, "sp_goods/detail.html", context)
        except:
            return redirect(reverse("sp_goods:IndexView"))

    def post(self, request):
        pass
