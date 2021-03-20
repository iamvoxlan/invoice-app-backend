from authentication.models import Users
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'password', 'role']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    def create(self, validated_data):
        return Users.objects.create_user(validated_data['username'], validated_data['role'], validated_data['password'])

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)