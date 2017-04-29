from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(?P<feed_id>[0-9]+)/$', views.printFeed, name='printFeed'),
    url(r'(?P<feed_id>[0-9]+)/postItem/$', views.postItem, name='postItem'),
    url(r'createAccount/$', views.createAccount, name='createAccount'),
]
