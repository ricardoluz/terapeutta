from django.urls import path
from .views import (
    login_usuario,
    logout_usuario,
    registro_usuario,
)


urlpatterns = [
    path("registro/", registro_usuario, name="registro_usuario"),
    path("login/", login_usuario, name="login"),
    path("logout/", logout_usuario, name="logout"),
    path("login/", login_usuario, name="autenticacao_login"),
    path("logout/", logout_usuario, name="autenticacao_logout"),
]
