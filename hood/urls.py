from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
   url(r'^$',views.home,name = 'home'),
   url(r'^search/', views.search_results, name='search_results'),
   url(r'^join/(\d+)',views.join,name = 'join'),
   url(r'^profile/(\d+)', views.profile, name='profile'),
   url(r'^editprofile/',views.edit_profile,name = 'edit_profile'),
   url(r'^exithood/(\d+)',views.exitHood,name = 'exit'),
   url(r'^newpost/',views.new_post,name = 'new_post'),
   url(r'^add/buss$', views.new_buss, name='new_buss'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)