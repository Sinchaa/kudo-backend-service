from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from kudos_app.serializers import UserSerializer

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # For demo: return user id and organization
                serializer = UserSerializer(user, many=False)
                return Response(serializer.data)
            else:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)