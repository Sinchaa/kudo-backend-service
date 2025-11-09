from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Kudo, User
from .serializers import KudoSerializer, UserSerializer

def get_current_user(request):
    # For demo: get user from request (e.g., header or session)
    # Replace with real authentication in production
    user_id = request.query_params.get('user_id')
    return User.objects.get(id=user_id)

class GiveKudoView(APIView):
    permission_classes = []

    def post(self, request):
        user = get_current_user(request)
        kudos_to_id = request.data.get('kudos_to_id')
        message = request.data.get('message', '')
        # Check if user has kudos left this week
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())
        kudos_given = Kudo.objects.filter(kudos_from=user, created_at__gte=start_of_week).count()
        if kudos_given >= 3:
            return Response({'error': 'No kudos left to give this week.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            kudos_to = User.objects.get(id=kudos_to_id)
        except User.DoesNotExist:
            return Response({'error': 'kudos_to not found.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if kudos_to == user:
            return Response({'error': 'Cannot give kudo to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        kudo = Kudo.objects.create(kudos_from=user, kudos_to=kudos_to, message=message)
        serializer = KudoSerializer(kudo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReceivedKudosListView(APIView):
    permission_classes = []

    def get(self, request):
        user = get_current_user(request)
        print(user)
        received_kudos = Kudo.objects.filter(kudos_to=user).order_by('-created_at')
        print(received_kudos)
        serializer = KudoSerializer(received_kudos, many=True)
        return Response(serializer.data)

class GivenKudosListView(APIView):
    permission_classes = []

    def get(self, request):
        user = get_current_user(request)
        given_kudos = Kudo.objects.filter(kudos_from=user).order_by('-created_at')
        serializer = KudoSerializer(given_kudos, many=True)
        return Response(serializer.data)

class AvailableKudosView(APIView):
    permission_classes = []

    def get(self, request):
        user = get_current_user(request)
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())
        kudos_given = Kudo.objects.filter(kudos_from=user, created_at__gte=start_of_week).count()
        kudos_left = max(0, 3 - kudos_given)
        return Response({'kudos_left': kudos_left})
    
class FetchUsersListView(APIView):
    permission_classes = []

    def get(self, request):
        user = get_current_user(request)
        print(user.organization)
        users_list = User.objects.filter(organization=user.organization).exclude(id=user.id)
        serializer = UserSerializer(users_list, many=True)
        return Response(serializer.data)

