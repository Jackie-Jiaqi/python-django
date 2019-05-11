"""IDD_WEB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('app.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url



urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^index/$', views.index, name='index'),
    url(r'^$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    url(r'^charts/$', views.charts, name='charts'),
    url(r'^new_mongo_connection/$', views.new_mongo_connection, name='new_mongo_connection'),
    url(r'^new_json_connection/$', views.new_json_connection, name='new_json_connection'),
    url(r'^new_csv_connection/$', views.new_csv_connection, name='new_csv_connection'),
    url(r'^new_excel_connection/$', views.new_excel_connection, name='new_excel_connection'),
    url(r'^view_data/$', views.view_data, name='view_data'),
    url(r'^data_list/$', views.data_list, name='data_list'),
    path('dashboard/', include('dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
