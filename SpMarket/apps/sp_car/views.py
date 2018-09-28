from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from db.base_view import BaseVerifyView
from sp_car.helper import get_car_key
from sp_goods.models import GoodsSKU
from django_redis import get_redis_connection

"""
    添加购物车
    1. 使用post方式
    2. post中完成的内容
        a. 首先判断是否登录
            user_id = request.session.get("ID")
            
            没有登录,跳转到登录页面
            
        a. 接收参数 request.POST
            参数:
                sku_id 商品sku_id
                count 添加的数量
                
            判断参数的合法性:
                1. 都要是整数
                2. 商品必须要存在
                3. 库存判断
                
        b. 每个人的购物车都不一样
            如何确保每个人购物车不一致(购物车放redis)
            链接redis, 操作
            
            使用redis中的hash对象保存购物车
            hset key field value
            hset car_user_id sku_id count sku_id2 count2  ...........
            每条记录都要有两个字段
            sku_id 
            count 
            
            
            添加购物车的时候, 有两种情况:
                判断购物车中是否有sku_id,如果有在元有的基础上 对count进行添加,
                没有直接添加
        c. 添加成功 返回
            该用户购物车中商品的总数量
     
"""


# addCar/
class AddCarView(View):
    def get(self, request):
        pass

    def post(self, request):
        # 1. 判断用户是否登录
        user_id = request.session.get("ID")
        if user_id is None:
            return JsonResponse({"error": 1, "msg": "没有登录,请登录!"})

        # 2. 接收请求参数
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")

        # 判断参数合法性
        # 1.都要是整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse({"error": 2, "msg": "参数错误!"})

        # 2.商品必须要存在
        try:
            goods_sku = GoodsSKU.objects.get(pk=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"error": 3, "msg": "商品不存在!"})

        # 3.库存判断
        if goods_sku.stock < count:
            return JsonResponse({"error": 4, "msg": "库存不足!"})

        # 将购物车数据添加到redis中
        # 链接redis
        cnn = get_redis_connection("default")
        # 操作redis
        # 准备key
        car_key = get_car_key(user_id)
        # 添加数据到购物车
        cnn.hincrby(car_key, sku_id, count)

        # 获取购物车中的总的商品的数量
        car_values = cnn.hvals(car_key)  # 保存到redis中的数据是 二进制编码了, 需要解码才能使用
        total = 0
        for v in car_values:
            total += int(v)
        # print(car_values)

        return JsonResponse({"error": 0, "msg": "添加成功", "total": total})


"""
    减购物车
"""


# del_car
class DelCarView(View):
    def get(self, request):
        pass

    def post(self, request):
        # 1. 判断用户是否登录
        user_id = request.session.get("ID")
        if user_id is None:
            return JsonResponse({"error": 1, "msg": "没有登录,请登录!"})

        # 2. 接收请求参数
        sku_id = request.POST.get("sku_id")
        count = -1

        # 判断参数合法性
        # 1.都要是整数
        try:
            sku_id = int(sku_id)
        except:
            return JsonResponse({"error": 2, "msg": "参数错误!"})

        # 2.商品必须要存在
        try:
            goods_sku = GoodsSKU.objects.get(pk=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"error": 3, "msg": "商品不存在!"})

        # 从购物车中减去商品数量
        # 链接redis
        cnn = get_redis_connection("default")
        # 操作redis
        # 准备key
        car_key = get_car_key(user_id)
        # 从购物车的数量减
        cnn.hincrby(car_key, sku_id, count)
        # 如果商品sku_id对应的数量为0,就从购物车中删除该商品sku_id
        count = cnn.hget(car_key, sku_id)
        if int(count) < 1:
            cnn.hdel(car_key, sku_id)

        # 获取购物车中的总的商品的数量
        car_values = cnn.hvals(car_key)  # 保存到redis中的数据是 二进制编码了, 需要解码才能使用
        total = 0
        for v in car_values:
            total += int(v)

        return JsonResponse({"error": 0, "msg": "减少成功", "total": total})


"""
    购物车展示页面
"""


# car/
class CarShowView(BaseVerifyView):
    def get(self, request):
        """
            获取购物车数据:
            1,购物车中的商品数据
                存放在redis中  sku_id count
                根据sku_id 查询出商品数据

                返回应该返回一个列表(所有的商品数据)

            2,所有商品的总价格和总数量
        """
        user_id = request.session.get('ID')

        # 准备两个变量
        total_price = 0  # 总价格
        total_count = 0  # 总数量

        # 1. 购物车中的商品数据

        # 链接到redis
        cnn = get_redis_connection("default")
        # 从redis中获取购物车信息
        # 准备car_key
        car_key = get_car_key(user_id)
        # 取数据
        cars = cnn.hgetall(car_key)  # 获取的是一个字段,遍历字典
        # print(cars)

        # 准备一个变量 , 列表类型数据 ,保存多个商品
        goodsList = []
        for sku_id, count in cars.items():
            # print(sku_id,count)
            sku_id = int(sku_id)  # 商品id
            count = int(count)  # 购物车数量

            # 获取商品的数据
            goods_sku = GoodsSKU.objects.get(pk=sku_id)

            # 需要购物车中商品的数量, 我们可以在goods_sku对象上新添加一个属性
            goods_sku.count = count

            # 将该商品保存到商品列表中
            goodsList.append(goods_sku)

            # 处理总价格和总数量
            total_price += goods_sku.price*count
            total_count += count

        # 2,所有商品的总价格和总数量

        # 构造字段 渲染数据
        context = {
            "goodsList": goodsList,
            "total_price": total_price,
            "total_count": total_count,
        }
        return render(request, "sp_car/shopcart.html", context)

    def post(self, request):
        pass
