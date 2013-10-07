from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'catalog.views.main'),
	url(r'^catalog/$', 'catalog.views.main'),
	url(r'^catalog/(?P<sort>[A-Za-z0-9_-]+)/$', 'catalog.views.catalog'),
	url(r'^catalog/(?P<sort>[A-Za-z0-9_-]+)/(?P<page>[0-9]+)/$', 'catalog.views.catalog'),
	url(r'^admin/$', 'ad.views.admin_main'),
	url(r'^admin/catalog/$', 'ad.views.admin_main'),
	url(r'^admin/catalog/(?P<sort>[A-Za-z0-9_-]+)/$', 'ad.views.admin_catalog'),
	url(r'^admin/catalog/(?P<sort>[A-Za-z0-9_-]+)/(?P<page>[0-9]+)/$', 'ad.views.admin_catalog'),
	url(r'^admin/edit/(?P<item>[A-Za-z0-9_-]+)/$', 'ad.views.admin_edit'),
	url(r'^admin/add/$', 'ad.views.admin_add'),
	url(r'^admin/catalog/(?P<sort>[A-Za-z0-9_-]+)/$', 'ad.views.admin_catalog'),
	url(r'^admin/delete/(?P<item>[A-Za-z0-9_-]+)/$', 'ad.views.admin_delete'),
	url(r'^(?P<item>[A-Za-z0-9_-]+)/$', 'catalog.views.item'),

)
