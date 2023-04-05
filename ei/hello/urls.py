from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'), #path名取得→ここでは'ryuichiが変数名となっている．原則はhelloのアプリだからね！！'
    path('reverse',views.reverse, name='reverse'),
    path('create',views.create, name='create'),
    path('think',views.think,name='think'),
    path('message/<int:num>',views.message,name='message'),
    path('medelete',views.medelete,name='medelete'),
    path('delete/<int:num>',views.delete,name='delete'),
    path('update/<int:num>',views.delete,name='update'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('follow', views.follow, name='follow'),
    path('favorite', views.favorite, name='favorite'),
    path('gooddelete/<int:num>',views.gooddelete,name='gooddelete'),
    path('whogood', views.whogood, name='whogood'),
    path('finduser', views.finduser, name='finduser'),
    path('add',views.add,name='add'),
    path('god/<int:anime_id>',views.god,name='god'),
    
]









