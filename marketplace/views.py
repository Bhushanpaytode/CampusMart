from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category, Order


def home(request):
    products = Product.objects.order_by("-created_at")[:6]
    return render(request, "home.html", {"products": products})


def products(request):
    product_list = Product.objects.all().order_by("-created_at")

    query = request.GET.get("q")
    category_id = request.GET.get("category")

    if query:
        product_list = product_list.filter(name__icontains=query)

    if category_id:
        product_list = product_list.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, "products.html", {
        "products": product_list,
        "categories": categories,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {
        "product": product
    })


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        from django.contrib.auth.models import User

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("home")

    return render(request, "register.html")


@login_required
def sell_product(request):
    if request.method == "POST":
        product = Product.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            category_id=request.POST.get("category"),
            condition=request.POST.get("condition"),
            seller=request.user,
            image=request.FILES.get("image"),
        )

        return redirect("product_detail", pk=product.pk)

    return render(request, "sell_product.html", {
        "categories": Category.objects.all()
    })


@login_required
def my_listings(request):
    products = Product.objects.filter(
        seller=request.user
    ).order_by("-created_at")

    return render(request, "my_listings.html", {
        "products": products
    })


@login_required
def buy_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.seller == request.user:
        messages.error(request, "You cannot buy your own product.")
        return redirect("product_detail", pk=pk)

    Order.objects.create(
        product=product,
        buyer=request.user,
        quantity=1,
        total_price=product.price,
    )

    messages.success(request, "Order placed successfully!")
    return redirect("my_orders")


@login_required
def my_orders(request):
    orders = Order.objects.filter(
        buyer=request.user
    ).order_by("-order_date")

    return render(request, "my_orders.html", {
        "orders": orders
    })