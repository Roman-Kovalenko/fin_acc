# from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegisterForm(UserCreationForm):
    """
    Форма для регистрации пользователя
    """
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ('email', 'name', 'patronymic', 'surname')
