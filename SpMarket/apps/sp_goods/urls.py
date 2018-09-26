from django.conf.urls import url
from sp_goods.views import (IndexView,
                            CategoryView,
                            DetailView,
                            )

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='IndexView'),  # 首页
    url(r'^category/$', CategoryView.as_view(), name='CategoryView'),  # 列表
    url(r'^detail/(?P<sku_id>\d+)/$', DetailView.as_view(), name='DetailView'),  # 详情
]
