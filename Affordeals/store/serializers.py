from .models import SiteUser
from rest_framework import serializers


class SiteUserSerializer(serializers.ModelSerializer):
  user_id = serializers.IntegerField(read_only=True)
  class Meta:
    model = SiteUser
    fields = ['id', 'user_id', 'birth_date', 'phone_number']


