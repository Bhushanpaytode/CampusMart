from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.products, name="products"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("sell/", views.sell_product, name="sell_product"),
    path("my-listings/", views.my_listings, name="my_listings"),
    path("buy/<int:pk>/", views.buy_product, name="buy_product"),
    path("my-orders/", views.my_orders, name="my_orders"),
]
