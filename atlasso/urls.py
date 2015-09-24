from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

from .views import crowd_session_view, logout_view, AtlassoView

urlpatterns = patterns('',
    url(r'', include('kompassi_oauth2.urls')),
    url(r'^$', AtlassoView.as_view(template_name='index.jade'), name='index_view'),
    url(r'^error/?$', AtlassoView.as_view(template_name='error.jade'), name='error_view'),
    url(r'^admin$', RedirectView.as_view(url='/admin/'), name='admin_redirect_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crowd/?$', crowd_session_view, name='crowd_session_view'),
    url(r'^logout/?$', logout_view, name='logout_view'),
)
