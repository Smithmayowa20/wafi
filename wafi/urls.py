"""wafi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from registration.backends.simple.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
from app.forms import MyRegForm

from app import views

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        # the named URL that we want to redirect to after
        # successful registration
        return ('add_money')

urlpatterns = [
    url('admin/', admin.site.urls),
    url('add_money/', views.add_money, name="add_money"),
    url('send_money/', views.send_money, name="send_money"),
    url('withdraw_money/', views.withdraw_money, name="withdraw_money"),
]

urlpatterns = urlpatterns + [
    url(r'^accounts/register/$', MyRegistrationView.as_view(form_class=MyRegForm), name='registration_register'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
]
