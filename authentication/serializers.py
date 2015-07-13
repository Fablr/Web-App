from rest_framework import serializers
from django.contrib.auth.models import User, Group
from authentication.models import UserProfile

# first we define the serializers
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
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'city', 'state_province', 
        )

    def restore_object(self, attrs, instance=None):
        profile = super(UserProfileSerializer, self).restore_object(
            attrs, instance
        )

        if profile:
            user = profile.user

            user.email = attrs.get('user.email', user.email)
            user.first_name = attrs.get('user.first_name', user.first_name)
            user.last_name = attrs.get('user.last_name', user.last_name)

            user.save()

        return profile
