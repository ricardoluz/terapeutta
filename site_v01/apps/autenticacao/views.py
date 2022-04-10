from django.shortcuts import redirect, render

from django.contrib.auth.models import Group, User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from ..core.models import Terapeuta

from .forms import CreateUserForm_v01, LoginUserForm
from .decorators import somente_usuario_nao_autenticado, allowed_users_v01


@somente_usuario_nao_autenticado
def login_usuario(request):

    form = LoginUserForm()

    if request.method == "POST":
        form = LoginUserForm(request="POST")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        # if form.is_valid():
        #     return redirect('home')

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            messages.info(request, "e-mail OU senha incorreta.")

    context = {"form": form}

    return render(request, "autenticacao/login.html", context)



@somente_usuario_nao_autenticado
def login_usuario_v01(request):

    form = LoginUserForm()

    if request.method == "POST":
        form = LoginUserForm(request="POST")
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
# https://stackoverflow.com/questions/26857686/django-crispy-forms-error-message Rever
# TODO: Rever com estes conceitos.
        else:
            messages.info(request, "e-mail OU senha incorreta.")

    context = {"form": form}

    return render(request, "autenticacao/login.html", context)


@somente_usuario_nao_autenticado
def registro_usuario(request):

    form = CreateUserForm_v01()
    if request.method == "POST":

        form = CreateUserForm_v01(request.POST)

        # email_form = form.cleaned_data['email']
        # TODO: Passar a solução cadastrado para o forms. Melhorar a solução.
        email_form = request.POST.get("email")
        if User.objects.filter(email=email_form).exists():
            messages.error(request, "Já existe este e-mail cadastrado.")
            context = {"form": form}
            return render(request, "autenticacao/register.html", context)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            group = Group.objects.get(name="terapeuta")
            user.groups.add(group)

            Terapeuta.objects.create(
                user=user,
                #     name=user.username,
            )

            messages.success(request, "Uma conta foi criada para " + username)

            return redirect("login")

    context = {"form": form}
    return render(request, "autenticacao/register.html", context)


@allowed_users_v01()
def logout_usuario(request):
    logout(request)
    return redirect("home")
