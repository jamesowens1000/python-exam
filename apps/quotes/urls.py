from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'logout$', views.logout),
    url(r'edit_page$', views.edit_page),
    url(r'users/update$', views.update),
    url(r'^quotes$', views.quotes),
    url(r'post_quote$', views.post_quote),
    url(r'user/(?P<user_id>\d+)$', views.user_quotes),
    url(r'like_quote/(?P<quote_id>\d+)$', views.like_quote),
    url(r'delete/(?P<quote_id>\d+)$', views.delete_quote),
]