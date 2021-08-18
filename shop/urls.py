from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProductListView.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='registration'),
    path('logout/', Logout.as_view(), name='logout'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('update_product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('returns/', ReturnsView.as_view(), name='returns'),
    path('purcase/', PurcaseView.as_view(), name='purcase_user'),
    path('returns/delete/<int:pk>/', ReturnDeleteView.as_view(), name='return-delete'),
    path("product/about/<int:pk>/", ProductAbout.as_view(), name="about"),
    path("product/buy/<int:pk>", ProductBuy.as_view(), name="buy_product"),
    path("return/", Returns.as_view(), name="return"),
     path('returns/confirm/<int:pk>', Confirm.as_view(), name = 'confirm'),
]