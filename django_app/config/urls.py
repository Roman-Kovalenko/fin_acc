from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


# TODO: Настроить раздачу боевой статики
urlpatterns = [
    path('admin/', admin.site.urls),
    # TODO: Замена на 'finance:transaction:main' в будущем
    path('home/', login_required(TemplateView.as_view(
        template_name='home.html',
        extra_context={'title': _('Main page')}
    )), name='home'),
    path('users/', include('users.urls')),
    path('finance/', include('finance.urls')),
]
