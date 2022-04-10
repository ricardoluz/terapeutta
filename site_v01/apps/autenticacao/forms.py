from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# from .models import Order, Customer


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class CreateUserForm_v01(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# class AutenticacaoForm_erro(ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         username = self.cleaned_data.get("username")
#         if (
#             email
#             and User.objects.filter(email=email).exclude(username=username).exists()
#         ):
#             raise Exception("Email addresses must be unique.")
#         return email


# class AutenticacaoForm(AuthenticationForm):
#     class Meta:
#         model = User
#         # fields = "__all__"
#         fields = ['username', 'password']


# class CustomerForm(ModelForm):
#     class Meta:
#         model = Customer
#         fields = '__all__'
#         exclude = ['user']
