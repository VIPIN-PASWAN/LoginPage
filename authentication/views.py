from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from LOGINPAGE import settings
# from django.conf import settings


def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!!")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Yours Account has been successfully created.")

        # WELCOME EMAIL
        subject = "Welcome to COMMUNITI.CO !"
        message = "Hello " + myuser.first_name + "!! \n" + "We are glad to welcome you.\n\n We have sent you a " \
                                                           "confirmation email, please confirm your email address in " \
                                                           "order to activate your account.\n\n Thank You.\n Stone " \
                                                           "Martin "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {"fname": fname})

        else:
            messages.error(request, "BAD CREDENTIALS !!")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully !")
    return redirect('home')
