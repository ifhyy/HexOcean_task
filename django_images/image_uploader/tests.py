import os

import tempfile

from PIL import Image as PILImage

from django.urls import reverse
from rest_framework.exceptions import ErrorDetail

from .models import CustomUser, AccountTier

from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class ImageUploaderTests(APITestCase):
    def setUp(self):

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_image_file:
            image = PILImage.new('RGB', (500, 5000))
            image.save(temp_image_file, 'JPEG')
            self.image_path = temp_image_file.name

        account_tier_basic = AccountTier.objects.create(name='basic',
                                                        thumbnail_sizes=(200))
        account_tier_basic.save()
        account_tier_enterprise = AccountTier.objects.create(name='enterprise',
                                                             thumbnail_sizes='200,400',
                                                             originally_uploaded_image=True,
                                                             generate_exp_links=True)
        account_tier_enterprise.save()

        user_test1 = CustomUser.objects.create(username='test1', password='1q2w3e',
                                               account_tier=account_tier_basic)
        user_test1.save()
        user_test2 = CustomUser.objects.create(username='test2', password='1q2w3e',
                                               account_tier=account_tier_enterprise)
        user_test2.save()

        self.client1 = APIClient()
        self.client1.force_login(user=user_test1)
        self.client2 = APIClient()
        self.client2.force_login(user=user_test2)

    def tearDown(self):
        os.remove(self.image_path)
        super().tearDown()

    def test_fail_views(self):
        response = self.client1.get(reverse('expiring_link'))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data, {'message': 'Link has expired.'})

#       check seralizer validators
        with open(self.image_path, 'rb') as image_file:
            response = self.client1.post(reverse('images_upload'), {'image': image_file,
                                                                    'expiring_time_seconds': 400}, format='multipart')
            self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEquals(response.data, {
                'non_field_errors': [ErrorDetail(
                    string='Your account permissions does not allow you to create expiring links', code='invalid')]})

        with open(self.image_path, 'rb') as image_file:
            response = self.client2.post(reverse('images_upload'), {'image': image_file,
                                                                    'expiring_time_seconds': 100}, format='multipart')
            self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEquals(response.data, {
                'expiring_time_seconds': [ErrorDetail(string='You can only specify time between 300 and 30000 seconds',
                                                      code='invalid')]})

        response = self.client1.get(reverse('images_upload'))
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_succeed_views(self):
        with open(self.image_path, 'rb') as image_file:
            response = self.client1.post(reverse('images_upload'), {'image': image_file}, format='multipart')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        with open(self.image_path, 'rb') as image_file:
            response = self.client2.post(reverse('images_upload'), {'image': image_file,
                                                                    'expiring_time_seconds': 300}, format='multipart')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        expiring_link = response.data['link']['expiring_link']
        response = self.client2.get(expiring_link)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


