from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Attendee
from .serializers import EventSerializer, AttendeeSerializer, UserRegistrationSerializer
from .tasks import send_registration_email
from django.shortcuts import get_object_or_404

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Користувач зареєстрований успішно"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['date', 'location', 'organizer']
    search_fields = ['title']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()

            print("Подія успішно створена.")

            return Response({"message": "Подію створено успішно", "event": EventSerializer(event).data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        event = get_object_or_404(Event, pk=event_id)

        attendee, created = Attendee.objects.get_or_create(user=request.user, event=event)
        if not created:
            return Response({"message": "Ви вже зареєстровані на цю подію."}, status=status.HTTP_400_BAD_REQUEST)

        #send_registration_email.delay(event.title, request.user.email)

        return Response({"message": "Реєстрація на подію успішна. Повідомлення надіслано на email."}, status=status.HTTP_201_CREATED)
