from django.conf.urls import patterns, url
from rango import views

urlpatterns= patterns(
              '',
              url(r'^$', views.index, name='index'),
              url(r'^about/$', views.about, name='about'),
              url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
              url(r'^add_category/$', views.add_category, name='add_category'), # NEW MAPPING!
              url(r'^category/(?P<category_name_url>\w+)$', views.category, name='category'),
              url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'),
              url(r'^register/$', views.register, name='register'),
              url(r'^login/$', views.user_login, name='login'),
              url(r'^restricted/', views.restricted, name='restricted'),
              url(r'^logout/$', views.user_logout, name='logout'),
              url(r'^profile/$', views.profile, name='profile'),
              url(r'^contact/$', views.contact, name='contact'),
              url(r'^update_profile/$', views.update, name='update'),
              url(r'^post_list/$', views.post_list, name='post_list'),
              url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
                  r'(?P<post>[-\w]+)/$', views.post_detail, name='post_detail'),
            url(r'^article/$', views.article, name='article'),

              )