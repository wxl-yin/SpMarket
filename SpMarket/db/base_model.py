from django.db import models


class BaseModel(models.Model):
    """
        基础模型类, 以后所有的模型类都可以继承该类
    """
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name="创建时间",
                                       )
    update_time = models.DateTimeField(verbose_name="创建时间",
                                       auto_now=True,
                                       )
    is_delete = models.BooleanField(verbose_name="是否删除",
                                    default=False,
                                    )

    class Meta:
        # 设置为抽象的类,只能被继承
        abstract = True
