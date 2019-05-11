from django.urls import path, re_path, include
from . import views
from .data_generator import insert_data
from . import dash_app_base_generic   # this loads the Dash app
from . import dash_layouts
from .dash_server import app, server
from django.contrib import admin
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from IDD_WEB import views as IDD_views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/admin/', admin.site.urls),

    re_path('^_dash-', views.dash_ajax),
    path('index/', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('<author_id>/team/', views.dashboard1, name='team'),
    path('<author_id>/player/', views.dashboard2, name='player'),
    path('<author_id>/body/', views.dashboard3, name='body'),
    path('<author_id>/playerload/', views.dashboard4, name='playerload'),
    path('livingstream/', views.livingstream, name='livingstream'),
    path('admin/', admin.site.urls),
    url(r'^index/$', IDD_views.index, name='index'),
    url(r'^$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    url(r'^charts/$', IDD_views.charts, name='charts'),
    url(r'^new_mongo_connection/$', IDD_views.new_mongo_connection, name='new_mongo_connection'),
    url(r'^new_json_connection/$', IDD_views.new_json_connection, name='new_json_connection'),
    url(r'^new_csv_connection/$', IDD_views.new_csv_connection, name='new_csv_connection'),
    url(r'^new_excel_connection/$', IDD_views.new_excel_connection, name='new_excel_connection'),
    url(r'^view_data/$', IDD_views.view_data, name='view_data'),
    url(r'^data_list/$', IDD_views.data_list, name='data_list'),

]
