from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .api_views import UserRegistrationView
from .api_views import EventViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', EventViewSet)

urlpatterns = [
    path('', views.event_list, name='event_list'),

    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/edit/', views.update_event, name='update_event'), 
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),

    path('create_event/', views.create_event, name='create_event'),

    path('register_event/<int:event_id>/', views.register_event, name='register_event'),

    path('register/', views.register_user, name='register_user'),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),

    path('logout/', LogoutView.as_view(), name='logout'),
    
]
