from rest_framework import serializers
from .models import User

"""
Here we mainly used ModelSerializer.We use this because it is simple to use when we have to serialize the data present
in our model. We get all data from our model by default.
"""


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    """
    write_only come in use when we update and create instance.This field is not going to serialize. 
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """
        This method is used to validate our data which we use in this serializer class.
        """
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password doesn't match")
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    This serializer is using for Profile based functionality.
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_no', 'email']


class UserChangePasswordSerializer(serializers.Serializer):
    """
    This serializer for change password functionality.
    """
    password = serializers.CharField(max_length=200, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=200, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        user.set_password(password)  # set_password convert our normal password format to hashable format
        user.save()
        return data
