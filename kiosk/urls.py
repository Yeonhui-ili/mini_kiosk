from django.urls import path, re_path
from . import views

app_name ="kiosk"

urlpatterns = [
    path("", views.MenuLV.as_view(), name="index"),
    path("menu/", views.MenuLV.as_view(), name='menu_list'),
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('get_order_info/', views.GetOrderInfo.as_view(), name='get_order_info'),
    path('process_order/', views.ProcessOrderView.as_view(), name='process_order'),
]