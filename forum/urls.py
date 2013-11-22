from django.conf.urls import *

urlpatterns = patterns('forum.views',
    url(r'^$', 'posts_recent', name='posts_recent'),
    url(r'^all/$','posts_all'),
    url(r'^categories/$','categories', name='categories'),
    url(r'^category/(?P<category_id>\w+)/$','category_posts', name='category'),
    url(r'^category/(?P<category_id>\w+)/newpost/$', 'post_new', name='post_new_cat'),
    url(r'^newpost/$', 'post_new', name='post_new'),
    url(r'^post/(?P<id>\d+)/(?P<title>\.+)/$', 'post', name='post_titled'),
    url(r'^post/(?P<id>\d+)/$', 'post', name='post'),
    url(r'^edit/(?P<id>\d+)/$', 'post_edit', name='post_edit'),
)
