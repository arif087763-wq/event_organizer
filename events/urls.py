#events/urls.py
from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path('organizer/dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('organizer/event/<slug:slug>/', views.organizer_event_detail, name='organizer_event_detail'),

    path('', views.event_list, name='event_list'),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
    path('<slug:slug>/register/', views.event_register, name='event_register'),
    path('<slug:slug>/payment/', views.event_payment, name='event_payment'),
    path('<slug:slug>/dashboard/', views.event_dashboard_participant, name='event_dashboard_participant'),
]

