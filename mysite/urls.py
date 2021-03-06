"""first_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib import admin
from django.conf.urls import  include, url
from django.conf.urls import url
from django.contrib import admin
from blog import views
import django.contrib.auth.views

urlpatterns = [
    url(r'admin/',admin.site.urls),
    url(r'^$',views.post_list,  name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^archives/$', views.archives, name='archives'),
    url(r'^tag/tag(?P<tag>\w+)/$', views.search_tag, name='search_tag'),
    url(r'^aboutme/$', views.about_me, name='about_me'),
    #url(r'^accounts/login/$',django.contrib.auth.views.login, name='login'),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^search/$', views.blog_search, name='search'),
    url(r'^user/user(?P<user_id>\w+)/$', views.search_user, name='search_user'),
    url(r'^register$', views.register_view,name='register'),
    url(r'^login$', views.login_view,name='login'),
]