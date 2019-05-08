
from django.contrib import admin
from django.conf.urls import url,include,static
from django.contrib import admin
from posts import views
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = "posts"
urlpatterns = [
    url(r'^$', views.post_home, name='post_home'),
    url(r'^create/', views.post_create, name='post_create'),
    url(r'^creates/', views.post_create, name='form'),
    url(r'^treemap/', views.map, name='map'),
    url(r'^create2/', views.post_create2, name='post_create2'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^(?P<id>[0-9]+)/$', views.post_detail,name='detail'),
    url(r'^QR/(?P<id>[0-9]+)/$', views.post_detail2,name='detail2'),
    url(r'^(?P<id>[0-9]+)/edit$', views.post_update,name='update'),
    url(r'^(?P<id>[0-9]+)/delete$', views.post_delete,name='delete'),
    url(r'^(?P<id>[0-9]+)/result$', views.test, name='result'),
    url(r'^(?P<id>[0-9]+)/re_bacteria', views.test, name='re_bacteria'),
    url(r'^QR/(?P<id>[0-9]+)/QRresult$', views.share, name='QRresult'),
    url(r'^Home/$', views.Home, name='home'),
    url(r'^about/$', views.post_about, name='about'),
    url(r'^bug_pic_gallery/$', views.bug_pic_gallery, name='category'),
    url(r'^search_name/$', views.search_bug_name, name='name'),
    url(r'^cabbagewhitefly/$', views.post_cabbagewhitefly, name='cabbagewhitefly'),
    url(r'^cabbagemoth/$', views.post_cabbagemoth, name='cabbagemoth'),
    url(r'^cabbageworms/$', views.post_cabbageworms, name='cabbageworms'),
    url(r'^citrusleafminer/$', views.post_citrusleafminer, name='citursleafminer'),
    url(r'^cutworm/$', views.post_cutworm, name='cutworm'),
    url(r'^europeanearwigs/$', views.post_europeanearwigs, name='europeanearwigs'),
    url(r'^japanesebeetle/$', views.post_japanesebeetle, name='japanesebeetle'),
    url(r'^mealybugs/$', views.post_mealybugs, name='mealybugs'),
    url(r'^psyllids/$', views.post_psyllids, name='psyllids'),
    url(r'^slugs/$', views.post_slugs, name='slugs'),
    url(r'^yellowaphids/$', views.post_yellowaphids, name='yellowaphids'),
    url(r'^leaf_pic_gallery/$', views.leaf_pic_gallery, name='gallery2'),
    url(r'^Banksia/$', views.post_Banksia, name='Banksia'),
    url(r'^Beech/$', views.post_Beech, name='Beech'),
    url(r'^Eucalyptus/$', views.post_Eucalyptus, name='Eucalyptus'),
    url(r'^Grevillea/$', views.post_Grevillea, name='Grevillea'),
    url(r'^Illawarra/$', views.post_Illawarra, name='Illawarra'),
    url(r'^Lilly/$', views.post_Lilly, name='Lilly'),
    url(r'^Moreton/$', views.post_Moreton, name='Moreton'),
    url(r'^Wattle/$', views.post_Wattle, name='Wattle'),
    url(r'^Willow/$', views.post_Willow, name='Willow'),
    url(r'^prevent/$', views.prevent, name='prevent'),


    url(r'^admin/', admin.site.urls),
    url(r'^managebugs/$',views.managebugs),


]
