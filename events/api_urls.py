from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import EventViewSet, AttendeeViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'attendees', AttendeeViewSet)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),

    path('', include(router.urls)),
    path('events/<int:event_id>/register/', AttendeeViewSet.as_view({'post': 'create'}), name='api_register_event'),
]
