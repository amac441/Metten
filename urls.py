from django.conf.urls.defaults import *
#from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.contrib import auth

from django.views.generic.list_detail import object_detail
from hitcount.views import update_hit_count_ajax
from rest_framework.urlpatterns import format_suffix_patterns



admin.autodiscover()

urlpatterns = patterns('',
	url(r'^ajax/hit/$', update_hit_count_ajax, name='hitcount_update_ajax'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'Metten.blog.views.index', name='home'),
    url(r'^plots$', 'Metten.blog.views.plots', name='plots'),
    url(r'^graph$', 'Metten.blog.views.graph', name='graph'),
    url(r'^linker$', 'Metten.blog.views.linker', name='linker'),
    url(r'^blog/', include('Metten.blog.urls')),
    url(r'^5years/', include('Metten.years.urls'))
)

urlpatterns += patterns(
	'django.contrib.auth.views',

	url(r'^login/$', 'login',  #this is django.contrib.views.login
		{'template_name': 'login.html'},
		name='5years_login'),

	url(r'^logout/$', 'logout',  #this is django.contrib.views.logout
		{'next_page': '/'},
		name='5years_logout'),

	url(r'^survey$', direct_to_template, {'template': 'survey.html'}),

	url(r'^metten$', direct_to_template, {'template': 'metten.html'}),

    # #static
    # (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #      {'document_root': settings.STATIC_ROOT}),

    # #media
    # (r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #      {'document_root': settings.MEDIA_ROOT}),

	)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()