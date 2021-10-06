import random

from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


def confirmation_code_generator():
    upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_case = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '1234567890'
    base = upper_case + lower_case + numbers
    length = 16
    confirmation_code = ''.join(random.sample(base, length))
    return confirmation_code


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать имя \'me\' в качестве username запрещено.'
            )
        return data

    def create(self, validated_data):
        user, status = User.objects.get_or_create(**validated_data)
        user.confirmation_code = confirmation_code_generator()
        user.save()
        return user
