from django.conf.urls import patterns, include, url

from message.views import MessageView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RyndaRebuild.views.home', name='home'),
    # url(r'^RyndaRebuild/', include('RyndaRebuild.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'message.views.list'),
    url(r'^login$', 'django.contrib.auth.views.login',\
        {'template_name': 'login.html'}),
    url(r'^logout$', 'message.views.logout_view'),
    url(r'^vse$', 'message.views.all'),
    url(r'^pomogite$', 'message.views.requests'),
    url(r'^pomogu$', 'message.views.offer'),
    url(r'message/(?P<pk>\d+)$', MessageView.as_view()),
    ('^info/(?P<slug>[a-z_]+)$', 'core.views.infopages.show_page'),
    ('^info/s/(?P<id>\d+)$', 'message.views.show_message'),
    ('^pomogite/dobavit', 'message.views.add_request_form'),
)

urlpatterns += patterns('core.views',

)

urlpatterns += patterns('',
    (r'^api/', include('api.urls')),
)
