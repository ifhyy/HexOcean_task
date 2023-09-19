from django.core.files.base import ContentFile
from django.core.files import File
from django.urls import reverse
from rest_framework import serializers

from .models import Image, CustomUser
from PIL import Image as PILImage
from io import BytesIO


class ImageSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    size = serializers.CharField(max_length=10, read_only=True)
    image = serializers.ImageField()

    def to_representation(self, instances):
        if not isinstance(instances, list):
            instances = [instances]

        serialized_data = []

        for instance in instances:
            data = super().to_representation(instance)
            data['size'] = data['size']+'px' if not data['size'] == 'original' else data['size']
            serialized_data.append(data)

        return serialized_data

    def get_image(self, image):
        request = self.context.get('request')
        image_url = image.image.url
        return request.build_absolute_uri(image_url)

    def validate_image(self, image):
        valid_formats = ['image/jpeg', 'image/png']
        if image.content_type not in valid_formats:
            raise serializers.ValidationError('Invalid image format. Only JPG and PNG are allowed')
        return image



