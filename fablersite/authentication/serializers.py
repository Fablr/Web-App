from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import UserProfile

from feed.models import Following

'''
Deprecated Serializer that should be removed for production.
'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        write_only_fields = ['password']

    def create(self, attrs, instance=None):
        user = User(username=attrs['username'], email=attrs['email'], is_staff=False, is_active=True, is_superuser=False)
        user.set_password(attrs['password'])
        user.save()
        return user

    def update(self, attrs, instance=None):
        user = instance
        user.username = attrs['username']
        user.email = attrs['email']
        user.set_password(attrs['password'])
        user.save()
        return user

    def validate(self, attrs):
        '''
        Make sure email is unique. This is shitty, yes, but allows us to not create custom user class.
        '''
        if 'email' not in attrs:
            raise serializers.ValidationError("Email required for registration.")
        if User.objects.filter(email=attrs['email']).exclude(username=attrs['username']).count():
            raise serializers.ValidationError("Email must be unique.")
        return attrs

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group

class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.pk', read_only=True)
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.CharField(source='user.email', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    currentUser = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    def get_currentUser(self, profile):
        request = self.context.get('request', None)
        return (request.user.pk == profile.pk)

    def get_following(self, profile):
        result = False
        request = self.context.get('request', None)
        if request is not None:
            follower = request.user
            following = profile.user
            try:
                instance = Following.objects.get(follower=follower, following=following)
                result = True
            except ObjectDoesNotExist:
                pass
        return result

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'currentUser', 'following', 'birthday', 'city', 'state_province', 'image')

    def create(self, attrs, instance=None):
        assert 'username' in attrs, (
            'Missing required field `username`.'
        )

        assert 'email' in attrs, (
            'Missing required field `email`.'
        )

        assert 'password' in attrs, (
            'Missing required field `password`.'
        )

        user = User(username=attrs['username'], email=attrs['email'], is_staff=False, is_active=True, is_superuser=False)
        user.set_password(attrs['password'])
        user.save()
        instance = UserProfile.objects.get(user=user)
        return instance

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data is not None:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            try:
                instance.user.full_clean()
                if 'email' in user_data:
                    if User.objects.filter(email=instance.email).exclude(pk=instance.pk).count():
                        raise serializers.ValidationError("Field `Email` must be unique.")
            except DjangoValidationError as exc:
                raise serializers.ValidationError(detail=serializers.get_validation_error_detail(exc))
            instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
