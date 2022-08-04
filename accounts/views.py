from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django_rest_passwordreset.views import (ResetPasswordRequestToken, ResetPasswordConfirm,
                                             ResetPasswordValidateToken)
from .models import User
from accounts.serializer import (UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
                                 UserChangePasswordSerializer, DeliverBoyRegistrationSerializer)


# generating custom token

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    """
    This method is used for generating token. 
    """

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.


class UserRegistration(APIView):
    """
    User Registration view.
    """

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token": token, "msg": "done"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryBoyRegistration(APIView):
    """
    User Registration view.
    """

    def post(self, request, format=None):
        serializer = DeliverBoyRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token": token, "msg": "done"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    User login view.
    """
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or password is not valid']}},
                                status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordView(APIView):
    """
    View for change password
    """

    permission_classes = [IsAuthenticated]
    """
    IsAuthenticated class used for verifying that user is must for this specified operation
    """

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(viewsets.ModelViewSet):
    """
    This is userprofile class in which we use ModelViewset. In this class we use different-different methods
    as per our requirement.
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


"""
Overriding of ResetPassword class to customize message part".

ResetPassword class works in three steps(token passing, token validation, token confirmation)
"""


class ResetPasswordConfirmView(ResetPasswordConfirm):
    """
    this is a customized part of ResetPasswordConfirm class.
    """

    def post(self, request, *args, **kwargs):
        super(ResetPasswordConfirmView, self).post(request, *args, **kwargs)
        return Response({'status': 'OK', 'message': ' Password Reset Successfully'})


class ResetPasswordValidateView(ResetPasswordValidateToken):
    """
    this is a customized part of ResetPasswordValidateToken class.
    """

    def post(self, request, *args, **kwargs):
        super(ResetPasswordValidateView, self).post(request, *args, **kwargs)
        return Response({'status': 'OK', 'message': ' Token validation succeed'})


class ResetPasswordTokenView(ResetPasswordRequestToken):
    """
    this is a customized part of ResetPasswordRequestToken class.
    """

    def post(self, request, *args, **kwargs):
        super(ResetPasswordTokenView, self).post(request, *args, **kwargs)
        return Response({'status': 'OK', 'message': ' Token Passed successfully'})



