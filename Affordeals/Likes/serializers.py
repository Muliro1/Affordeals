from .models import LikedItem
from rest_framework import serializers


class LikesSerializer(serializers.ModelSerializer):
  class Meta:
    model = LikedItem
    fields = ['user', 'object_id', 'content_type', 'content_object']