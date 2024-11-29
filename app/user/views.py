from rest_framework import generics, authentication, permissions
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system.

    Handles user registration by accepting POST requests with user data.
    Required fields:
    - email
    - password
    - name
    """

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user.

    Authenticates user credentials and returns an auth token.
    Required fields:
    - email
    - password

    Returns:
        Auth token that can be used for authenticated requests
    """

    serializer_class = AuthTokenSerializer
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user.

    Provides endpoints to:
    * Retrieve user profile
    * Update user details

    Authentication required.
    Users can only manage their own profile.
    """

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
