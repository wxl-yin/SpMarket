from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from sp_goods.models import (GoodsSKU, Category)
from django_redis import get_redis_connection


class IndexView(View):
    # 首页
    def get(self, request):
        return render(request, "sp_goods/index.html")

    def post(self, request):
        pass


"""
    1. 查询出了所有商品
    2. 查询出所有的分类,进行显示
    3. 点击某个分类,显示对应分类下的商品
        a. url中传递分类的id(需要通过url截取获取这个分类id)
            默认这个分类id为0,  默认展示的商品为第一个分类下的商品
        b. 根据分类id查询出对应的分类
        c. 根据查询出来的分类 查询出商品 分类对象.商品sku_set.all()
    4. 排序(综合,销量,价格,新品)
        设置一个参数: order = 0,1,2,3,4  ===>综合,销量,价格降序,价格升序,新品
        
        排序: 模型对象.objects.all().order_by("-字段")
        
        设置映射关系: ["id","-sale_num","-price","price","-create_time"]
"""


class CategoryView(View):
    # 列表页
    def get(self, request, cate_id=0, order=0):
        cate_id = int(cate_id)
        order = int(order)
        # 查询出所有的分类,进行显示
        categorys = Category.objects.filter(is_delete=False)

        # 获取是对应分类下的商品
        if cate_id == 0:
            # 默认展示第一个分类下的商品
            category = categorys.first()
            # 如果cate_id=0, cate_id就应该为该分类的pk
            cate_id = category.pk
        else:
            # 获取传入分类id对应的分类
            category = Category.objects.get(pk=cate_id)

        # goods_skus = GoodsSKU.objects.filter(is_delete=False)
        # 对应分类下的商品
        # 映射的关系
        order_by_rule = ["id", "-sale_num", "-price", "price", "-create_time"]
        goods_skus = category.goodssku_set.all().order_by(order_by_rule[order])



        # 获取该用户购物车中商品的总数
        user_id = request.session.get("ID", None)
        # 准备一个变量保存总数量
        total = 0
        if user_id:
            cnn = get_redis_connection("default")
            # 准备购物的键
            car_key = "car_%s" % user_id
            car_values = cnn.hvals(car_key)
            for v in car_values:
                total += int(v)



        # 组装一个字典
        context = {
            "goods_skus": goods_skus,
            "categorys": categorys,
            "cate_id": cate_id,
            "order": order,
            "total": total,
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
        except Exception as e:
            print(e)
            return redirect(reverse("sp_goods:IndexView"))

    def post(self, request):
        pass
