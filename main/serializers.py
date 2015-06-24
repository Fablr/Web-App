from rest_framework import serializers
from django.contrib.auth.models import User
from oauth2_provider.models import Application

class SignUpSerializer(serializers.ModelSerializer):
    client_id = serializers.SerializerMethodField()
    client_secret = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'password', 'client_id', 'client_secret')
        write_only_fields = ('password',)

    def get_client_id(self, obj):
        return Application.objects.get(user=obj).client_id 

    def get_client_secret(self, obj):
        return Application.objects.get(user=obj).client_secret


class LoginSerializer(SignUpSerializer):
    class Meta:
        model = User
        fields = ('client_id', 'client_secret')

