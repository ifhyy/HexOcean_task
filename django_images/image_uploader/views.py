from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
# from .serailizers import ImageUploadSerializer
from .models import Image, CustomUser



# class ImageViewSet(generics.CreateAPIView):
#     queryset = Image.objects.all()
#     parser_classes = (MultiPartParser,)
#     serializer_class = ImageUploadSerializer


