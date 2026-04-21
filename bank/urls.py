"""
URL configuration for bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from banking import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('user_login/', views.user_login, name='user_login'),
    path('welcome/', views.welcome, name='welcome'),
    path('accountcreate/', views.accountcreate, name='accountcreate'),
    path('balancecheck/', views.balancecheck, name='balancecheck'),
    path('depositamount/', views.depositamount, name='depositamount'),
    path('transactionhistory/', views.transactionhistory, name='transactionhistory'),
    path('transferamount/', views.transferamount, name='transferamount'),
    path('withdrawamount/', views.withdrawamount, name='withdrawamount'),
    path('deleteaccount/', views.deleteaccount, name='deleteaccount'),
    path('test-email/', views.test_email),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
]
