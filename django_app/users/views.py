from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .forms import UserRegisterForm


class SignUpView(SuccessMessageMixin, CreateView):
    """
    View для регистрации пользователя
    """
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = _('Your profile was created successfully')


# TODO: Заменить на нормальный профиль с возможностью редактирования
@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    """
    Временная затычка для отображения профиля пользователя
    """
    template_name = 'users/profile.html'
    extra_context={'title': _('User profile')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
