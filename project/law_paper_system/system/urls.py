from django.conf.urls import url
from . import views

#url包含一个域名，一个view，一个name
urlpatterns = [
    url(r'^$', views.main_window, name='main_window'),
    url(r'^paper/(?P<paper_id>[0-9]+)/$', views.paper_detail, name='paper_detail'),
    url(r'^paper_add/$', views.paper_add, name='paper_add'),
    url(r'search/$', views.search, name='search'),
    url(r'login/$', views.login, name='login'),
    url(r'delete/(?P<paper_id>[0-9]+)/$', views.delete, name='delete'),
]