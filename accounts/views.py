from django.shortcuts import render, redirect

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

User = get_user_model()


def signup_page(request):

    if request.method == "POST":

        mobile = request.POST.get("mobile_number")
        email = request.POST.get("email")
        if email:
            email = email.strip().lower()

        else:
            email = None

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            messages.error(request, "Passwords do not match")

            return render(request, "accounts/signup.html")

        if User.objects.filter(mobile_number=mobile).exists():

            messages.error(request, "Mobile number already registered")

            return render(request, "accounts/signup.html")

        if email:

            if User.objects.filter(email=email).exists():

                messages.error(request, "Email already registered")

                return render(request, "accounts/signup.html")

        user = User.objects.create_user(
            mobile_number=mobile,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")

        return redirect('accounts:login_page')

    return render(request, "accounts/signup.html")


def login_page(request):

    if request.method == "POST":

        login_input = request.POST.get("login")

        password = request.POST.get("password")

        login_input = login_input.strip().lower()
        try:

            if '@' in login_input:

                user_obj = User.objects.get(email=login_input)

            else:

                user_obj = User.objects.get(
                    mobile_number=login_input
                )

            user = authenticate(
                request,
                username=user_obj.get_username(),
                password=password
            )

            if user is not None:

                login(request, user)

                return redirect('core:home')

            else:

                messages.error(
                    request,
                    "Wrong password"
                )

        except User.DoesNotExist:

            messages.error(
                request,
                "User does not exist"
            )

    return render(
        request,
        "accounts/login.html"
    )

from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from orders.models import Order, Address


@login_required
def account_page(request):

    orders_count = Order.objects.filter(
        user=request.user
    ).count()

    addresses_count = Address.objects.filter(
        user=request.user
    ).count()

    recent_orders = Order.objects.filter(
        user=request.user
    )[:3]

    context = {

        'orders_count': orders_count,

        'addresses_count': addresses_count,

        'recent_orders': recent_orders,
    }

    return render(

        request,

        'accounts/account.html',

        context
    )

def logout_page(request):

    logout(request)

    return redirect('core:home')