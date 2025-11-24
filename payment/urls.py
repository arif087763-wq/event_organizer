from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
    path('<slug:slug>/register/', views.event_register, name='event_register'),
    path('<slug:slug>/payment/', views.event_payment, name='event_payment'),  # ⬅️ BARU
    path('<slug:slug>/dashboard/', views.event_dashboard_participant, name='event_dashboard_participant'),
]
