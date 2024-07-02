from djoser.serializers import UserSerializer as BaseUserSerializer,\
                               UserCreateSerializer as BaseUserCreateSerializer
                               

class UserCreateSerializer(BaseUserCreateSerializer):
  class Meta(BaseUserCreateSerializer.Meta):
    fields = ['id', 'username', 'email',
              'password', 'first_name',
              'last_name']

class UserSerializer(BaseUserSerializer):
  class Meta(BaseUserSerializer.Meta):
<<<<<<< HEAD
    fields = ['id', 'username', 'email', 'first_name', 'last_name']



=======
    fields = ['id', 'username', 'email',
              'first_name', 'last_name']
>>>>>>> api
