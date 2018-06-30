"""
 *  @ 创建者      zsh
 *  @ 创建时间    18-6-25 上午10:33
 *  @ 创建描述    
 *  
"""
from django.conf.urls import url

from meiduo_mall.apps.users.views import UserView, User2View

urlpatterns = [
    # 判断用户和手机的唯一性
    url(r'^username/count/$', UserView.as_view({"get": "username_iscount"})),
    url(r'^mobile/count/$', UserView.as_view({"get": "mobile_iscount"})),
    # 用户注册
    url(r'^register/$', UserView.as_view({"post": "register_user"})),
    url(r'^getall/$', User2View.as_view({"get": "list"})),
    url(r'^getall/(?P<pk>\d+)/$', User2View.as_view({"get": "retrieve"})),
    url(r'^getall/(?P<pk>\d+)/$', UserView.as_view({"get": "get_on_id"})),
    url(r'^getall/(?P<username>\w+)/$', UserView.as_view({"get": "get_on_name"})),
    url(r'^getall/(?P<mobile>\d+)/$', UserView.as_view({"get": "get_on_mobile"})),
    # url(r'username/(?P<user_name>\w{5,20})/count/$', UserView.as_view({"get": "username_iscount"})),

]
