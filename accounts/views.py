from django.shortcuts import render, redirect

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

User = get_user_model()


def signup_page(request):

    if request.method == "POST":

        mobile = request.POST.get("mobile_number")
        email = request.POST.get("email")
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

        try:

            if '@' in login_input:

                user_obj = User.objects.get(email=login_input)

            else:

                user_obj = User.objects.get(
                    mobile_number=login_input
                )

            user = authenticate(
                request,
                username=user_obj.mobile_number,
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

def logout_page(request):

    logout(request)

    return redirect('core:home')