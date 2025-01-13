from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserSerializer


class SignupView(APIView):
    """
    Consolidates Signup and Login functionality.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate tokens for the new user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Create the response with user data
            response = Response(serializer.data, status=status.HTTP_201_CREATED)

            # Determine if the environment is secure
            secure = not settings.DEBUG  # Use secure cookies only in production

            # Set the access token as an HttpOnly cookie
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=secure,
                samesite='Strict' if secure else 'Lax',
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            )

            # Set the refresh token as an HttpOnly cookie
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=secure,
                samesite='Strict' if secure else 'Lax',
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    """
    Consolidates Signin and Login functionality.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful'
            })

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Customizes the TokenObtainPairView to include secure cookie settings for tokens.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']

            # Determine if we are in production or development to set cookies securely
            secure = not settings.DEBUG  # Use secure cookies only in production
            response.set_cookie(
                'access_token',  # Access token cookie
                access_token,
                httponly=True,  # Prevent access to the cookie from JavaScript
                secure=secure,  # Send cookies over HTTPS only in production
                samesite='Strict' if secure else 'Lax',  # CSRF protection
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],  # Set expiration time
            )
            response.set_cookie(
                'refresh_token',  # Refresh token cookie
                refresh_token,
                httponly=True,  # Prevent access to the cookie from JavaScript
                secure=secure,  # Send cookies over HTTPS only in production
                samesite='Strict' if secure else 'Lax',  # CSRF protection
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],  # Set expiration time
            )

        return response