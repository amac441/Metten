from django.conf.urls.defaults import *
#from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib import auth
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'Metten.blog.views.index', name='home'),
    url(r'^plots$', 'Metten.blog.views.plots', name='plots'),
    url(r'^blog/', include('Metten.blog.urls'))
)

urlpatterns += patterns(
	'django.contrib.auth.views',

	url(r'^login/$', 'login',  #this is django.contrib.views.login
		{'template_name': 'login.html'},
		name='5years_login'),

	url(r'^logout/$', 'logout',  #this is django.contrib.views.logout
		{'next_page': '/'},
		name='5years_logout'),
	)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()