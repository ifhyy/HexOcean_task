import io
from django.core.cache import cache
from django.urls import reverse
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from PIL import Image as PILImage
from django.utils.http import urlencode

from .serailizers import ImageSerializer, URLSerializer
from .models import Image


def image_to_bytes(image_path):
    image = PILImage.open(image_path)
    image_buffer = io.BytesIO()
    image_format = 'PNG' if str(image_path).endswith('.png') else 'JPEG'
    image.save(image_buffer, format=image_format)
    image_bytes = image_buffer.getvalue()
    return image_bytes


class ExpiringLinkView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request):
        image_id = request.query_params.get('image_id')
        image_path = cache.get(f'image_{image_id}')

        if image_path:
            image_bytes = image_to_bytes(image_path)
            response = HttpResponse(content_type='image/jpeg')
            response.write(image_bytes)
            return response
        return Response({'message': 'Link has expired.'}, status=status.HTTP_404_NOT_FOUND)


class ImageAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = ImageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            image = serializer.validated_data['image']
            user = request.user
            user_account_tier = user.account_tier
            thumbnail_sizes = [int(size) for size in user_account_tier.thumbnail_sizes.split(',')]

            objects = []
            response_data = {}

            for size in thumbnail_sizes:
                obj = Image(image=image, user=user, size=size)
                obj.save()
                image_location = obj.image.path

                original_image = PILImage.open(image_location)
                original_width, original_height = original_image.size
                aspect_ratio = original_width / original_height
                desired_width = int(size * aspect_ratio)
                thumbnail_size = (desired_width, size)

                original_image.thumbnail(thumbnail_size)
                original_image.save(image_location)

                objects.append(obj)

            if user_account_tier.originally_uploaded_image:
                obj = Image(image=image, user=user, size='original')
                obj.save()

                objects.append(obj)

            serialized_objects = ImageSerializer(objects, many=True, context={'request': request})
            response_data['images'] = serialized_objects.data

            if user_account_tier.generate_exp_links and 'expiring_time_seconds' in self.request.data.keys():
                obj = objects[-1]
                image_id = obj.pk
                image_path = obj.image.path
                expiration_time = self.request.data['expiring_time_seconds']
                cache.set(f'image_{image_id}', image_path, int(expiration_time))
                base_url = reverse('expiring_link')
                query_params = urlencode({'image_id': image_id})
                link = f"{base_url}?{query_params}"
                serialized_link = URLSerializer(data={"expiring_link": link})
                serialized_link.is_valid()
                response_data['link'] = serialized_link.data

            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)