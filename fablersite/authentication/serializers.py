from rest_framework import serializers
from django.contrib.auth.models import User, Group
from authentication.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    currentUser = serializers.SerializerMethodField()

    def get_currentUser(self, user):
        request = self.context.get('request', None)
        return (request.user == user)

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
    currentUser = serializers.SerializerMethodField()

    def get_currentUser(self, profile):
        request = self.context.get('request', None)
        return (request.user.pk == profile.pk)

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'currentUser', 'birthday', 'city', 'state_province', 'image')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data is not None:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
