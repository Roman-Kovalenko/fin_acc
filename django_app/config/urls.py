from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


# TODO: Настроить раздачу боевой статики
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=settings.LOGIN_REDIRECT_URL)),
    path('users/', include('users.urls')),
    path('finance/', include('finance.urls')),
]
