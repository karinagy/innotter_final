from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'second_name', 'sex', 'role', 'email' 'is_blocked']


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True,
                         'required': True,
                         'validators': [validate_password]
                         }
        }

        def create(self, validated_data):
            return User.objects.create_user(**validated_data)
