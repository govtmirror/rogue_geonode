from django.conf.urls import include, patterns, url
from views import GetImage, ImageUpload

urlpatterns = patterns('',
    url(r'upload/?$', ImageUpload.as_view(), name='file_service_upload'),
    url(r'^(?P<key>[-\w\d\.]+?)$', GetImage.as_view(), name='file_service'),
    )
