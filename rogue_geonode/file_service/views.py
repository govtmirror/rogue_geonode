import json
from geonode.documents.views import document_download, document_upload
from geonode.documents.models import Document
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import get_list_or_404
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from geonode.utils import _get_basic_auth_info
from logging import getLogger

logger = getLogger(__name__)


class BasicAuthView(View):
    """
    A mixin that requires the user to be logged in or logs in the user with basic auth, if the appropriate headers are
    present, before rendering the response.
    """
    unauthenticated_response = HttpResponse("Unauthorized, please authenticate.", status=401)

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        logger.debug(self.request)
        if not user.is_authenticated() and self.request.META.get('HTTP_AUTHORIZATION'):
            try:
                logger.debug("User is not logged in, but the request has basic auth headers.  Attempting to log "
                             "the user in.")
                username, password = _get_basic_auth_info(self.request)
                user = authenticate(username=username, password=password)
                logger.debug("Able to log user in: {0}".format(user.is_authenticated()))

            except Exception, e:
                logger.debug(e)
                return self.unauthenticated_response

        return self.unauthenticated_response if not user.is_authenticated() else \
            super(BasicAuthView, self).dispatch(*args, **kwargs)


class GetImage(BasicAuthView):
    """
    Allows the user to download a document when providing the document's name.
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        title = kwargs.get('key')
        doc_id = get_list_or_404(Document, title=title)
        return document_download(request, doc_id[0].id)


class ImageUpload(BasicAuthView):
    """
    Allows users to upload documents using basic auth.
    """

    default_permissions = json.dumps(dict(authenticated="document_readwrite", users=list()))

    def get(self, request, *args, **kwargs):
        return document_upload(request)

    def post(self, request, *args, **kwargs):
        # Add the default permissions to the POST if they are missing.
        if not request.POST.get('permissions'):
            request.POST = request.POST.copy()
            request.POST.update(permissions=self.default_permissions)

        return document_upload(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ImageUpload, self).dispatch(*args, **kwargs)
