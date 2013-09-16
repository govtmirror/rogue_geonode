"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
import hashlib
import os
from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from geonode.documents.models import Document

class SimpleTest(TestCase):

    def setUp(self):
        user, created = User.objects.get_or_create(username='test_admin',
                                                   password='admin',
                                                   is_active=True)

        user.set_password('admin')
        user.save()

        self.user = user

    def test_index(self):
        """
        Test for the main view.
        """

        c = Client()
        response = c.get(reverse('file_service', kwargs=dict(key='test')))

        # Non-authenticated user should return 401
        self.assertEqual(response.status_code, 401)

        logged_in = c.login(username='test_admin', password='admin')
        self.assertTrue(logged_in)

        # An authenticated user should return a 404
        response = c.get(reverse('file_service', kwargs=dict(key='test')))
        self.assertEqual(response.status_code, 404)

        c.logout()

        # A client should get a 404 response with basic authorization
        headers = dict(HTTP_AUTHORIZATION="basic dGVzdF9hZG1pbjphZG1pbg==")
        response = c.get(reverse('file_service', kwargs=dict(key='test')), **headers )
        self.assertEqual(response.status_code, 404)

        # A client should get a 401 response with incorrect basic authorization
        headers = dict(HTTP_AUTHORIZATION="basic dGasdasdsabg==")
        response = c.get(reverse('file_service', kwargs=dict(key='test')), **headers )
        self.assertEqual(response.status_code, 401)

    def test_image_upload(self):
        """
        Tests uploading an image the file-service proxy creates a document.
        """

        c = Client()
        logged_in = c.login(username='test_admin', password='admin')
        permissions = json.dumps({"anonymous": "document_readonly",
                                  "authenticated": "document_readwrite",
                                  "users": list()})
        response = None
        title = None

        with open(os.path.join(settings.PROJECT_ROOT, 'static', 'img', 'logo.png'), 'rb') as f:
            title = '{0}.jpg'.format(hashlib.sha1(f.read()).hexdigest())
            uploaded = SimpleUploadedFile(title, f.read())
            data = dict(title=title, file=uploaded)
            response = c.post(reverse('file_service_upload'), data=data)

        self.assertEqual(1, Document.objects.filter(title=title).count())

        # Test downloading the file.
        response = c.get(reverse('file_service', kwargs=dict(key=title)))
        self.assertEqual(response.status_code, 200)

        Document.objects.filter(title=title).delete()

        # Requests with invalid keys should return a 404.
        response = c.get(reverse('file_service', kwargs=dict(key=title)))
        self.assertEqual(response.status_code, 404)

        # TODO: the basic auth views force users to login, but geonode documents
        # have permission levels for non-authenticated users.  It would be nice
        # to support all levels.













