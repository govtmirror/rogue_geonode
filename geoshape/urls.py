from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from geonode.urls import urlpatterns as geonode_url_patterns
from maploom.geonode.urls import urlpatterns as maploom_urls
from tilebundler.api import TilesetResource

tileset_resource = TilesetResource()

urlpatterns = patterns(
    '',
    (r'^file-service/', include('geoshape.file_service.urls')),
    (r'^tileset/', include('tilebundler.urls', namespace='tilesets')),
    (r'^api/', include(tileset_resource.urls)),
    (r'^proxy/', 'geoshape.views.proxy'),

    url(r'^security/$', TemplateView.as_view(template_name='security.html'), name='security'),
    url(r'^about/api/', TemplateView.as_view(template_name='api.html'), name='about_api'),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt')

)

urlpatterns += geonode_url_patterns
urlpatterns += maploom_urls
