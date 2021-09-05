
# from django.contrib.auth.models import User
from ..serializers import UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.


# Customizing JWT token claims
# by creating a subclass for the view and a subclass for its corresponding serializer.
# https: // django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    # overriding validate method to serialize more information

    def validate(self, attrs):
        data = super().validate(attrs)

        # include these information in the response so that we don't have to parse token
        # in the frontend to get the user id and make another request to get the user info.
        serialized_user_with_token = UserSerializerWithToken(self.user).data

        for k, v in serialized_user_with_token.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    # This user object will NOT be the usual user object Django attaches to the request.
    # Instead, the @api_view decorator will parse the user data from the token and add to request.
    user = request.user

    # Without permission decorator, user will still be able to make request without token
    # and this will throw an AttributeError because the user object is not populated with authenticated user info
    serialized_user = UserSerializer(user, many=False).data

    return Response(serialized_user)


@api_view(['GET'])
# No need for IsAuthenticated because if you're an admin user, you're authenticated.
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serialized_users = UserSerializer(users, many=True).data

    return Response(serialized_users)


@api_view(['POST'])
def registerUser(request):
    data = request.data

    try:
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password'])
        )
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    serialized_user_with_token = UserSerializerWithToken(user, many=False).data
    return Response(serialized_user_with_token)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    # get user from the access token
    user = request.user
    serialized_user_with_token = UserSerializerWithToken(user, many=False).data

    # get request body
    data = request.data

    # update username and email
    user.username = data['username']
    user.email = data['email']

    # update password only when it has a value
    if data['password'] != '':
        # hash password before save
        user.password = make_password(data['password'])

    user.save()

    return Response(serialized_user_with_token)
