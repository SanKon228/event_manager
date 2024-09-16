from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Attendee
from .forms import EventForm
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib.auth.views import LogoutView
from .tasks import send_registration_email

class CustomLogoutView(LogoutView):
    next_page = '/'

class CustomLoginView(LoginView):
    template_name = 'login.html'
    
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Ви успішно увійшли як {username}")
                return redirect('event_list')
            else:
                messages.error(request, "Невірне ім'я користувача або пароль")
        else:
            messages.error(request, "Невірне ім'я користувача або пароль")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)

            return redirect('event_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def event_list(request):
    events = Event.objects.all()

    # Отримання фільтрів з запиту
    search_query = request.GET.get('search', '')
    date_query = request.GET.get('date', '')
    location_query = request.GET.get('location', '')

    if search_query:
        events = events.filter(title__icontains=search_query)

    if date_query:
        try:
            parsed_date = parse_date(date_query)
            if parsed_date:
                events = events.filter(date=parsed_date)
            else:
                pass
        except ValueError:
            pass

    if location_query:
        events = events.filter(location__icontains=location_query)

    return render(request, 'event_list.html', {'events': events})

@login_required(login_url='/login/')
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    attendees = Attendee.objects.filter(event=event)
    
    if not request.user.is_authenticated:
        messages.error(request, 'Щоб переглянути деталі події, будь ласка, увійдіть у систему.')
        return redirect('/login/')
    
    return render(request, 'event_detail.html', {'event': event, 'attendees': attendees})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

def register_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    send_registration_email.delay(event.title, request.user.email)
    Attendee.objects.get_or_create(user=request.user, event=event)
    
    return redirect('event_detail', event_id=event_id)
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if event.organizer != request.user:
        return HttpResponseForbidden("Ви не маєте прав для видалення цієї події.")

    if request.method == 'POST':
        event.delete()
        messages.success(request, "Подію видалено успішно.")
        return redirect('event_list')

    return render(request, 'event_confirm_delete.html', {'event': event})

@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if request.user != event.organizer:
        return redirect('event_list') 

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'event_form.html', {'form': form, 'event': event})