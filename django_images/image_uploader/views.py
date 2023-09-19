import copy

from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from PIL import Image as PILImage
from io import BytesIO

from .serailizers import ImageSerializer
from .models import Image, CustomUser


class ImageAPIView(APIView):

    def get(self, request):
        return Response({'it': 'works'})

    def post(self, request):
        serializer = ImageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            image = serializer.validated_data['image']
            user = request.user
            user_account_tier = user.account_tier
            thumbnail_sizes = [int(size) for size in user_account_tier.thumbnail_sizes.split(',')]

            objects = []

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
            return Response(serialized_objects.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

