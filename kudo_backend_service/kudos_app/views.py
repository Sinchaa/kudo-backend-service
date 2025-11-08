from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import Kudo, User
from .serializers import KudoSerializer

def get_current_user(request):
    # For demo: get user from request (e.g., header or session)
    # Replace with real authentication in production
    user_id = request.query_params.get('user_id')
    return User.objects.get(id=user_id)

class GiveKudoView(APIView):
    permission_classes = []

    def post(self, request):
        user = get_current_user(request)
        receiver_id = request.data.get('receiver_id')
        message = request.data.get('message', '')
        # Check if user has kudos left this week
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())
        kudos_given = Kudo.objects.filter(sender=user, created_at__gte=start_of_week).count()
        if kudos_given >= 3:
            return Response({'error': 'No kudos left to give this week.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({'error': 'Receiver not found.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if receiver == user:
            return Response({'error': 'Cannot give kudo to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        kudo = Kudo.objects.create(sender=user, receiver=receiver, message=message)
        serializer = KudoSerializer(kudo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReceivedKudosListView(APIView):
    permission_classes = []

    def get(self, request):
        user = get_current_user(request)
        print(user)
        received_kudos = Kudo.objects.filter(receiver=user).order_by('-created_at')
        print(received_kudos)
        serializer = KudoSerializer(received_kudos, many=True)
        return Response(serializer.data)

class GivenKudosListView(APIView):
    permission_classes = []

    def get(self, request):
        user = get_current_user(request)
        given_kudos = Kudo.objects.filter(sender=user).order_by('-created_at')
        serializer = KudoSerializer(given_kudos, many=True)
        return Response(serializer.data)

class AvailableKudosView(APIView):
    permission_classes = []

    def get(self, request):
        user = get_current_user(request)
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())
        kudos_given = Kudo.objects.filter(sender=user, created_at__gte=start_of_week).count()
        kudos_left = max(0, 3 - kudos_given)
        return Response({'kudos_left': kudos_left})