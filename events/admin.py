from django.contrib import admin
from .models import Event,EventRegistration,Ticket

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
  list_display=('title','organizer','start_datetime','is_published','price')
  prepopulated_fields={"slug": ("title",)}
  list_filter=('is_published','start_datetime')
  search_fields=('title','description','location')

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
  list_display=('event','participant','status','registered_at','checked_in')
  list_filter=('status','checked_in')
  search_fields=('event__title','participant__username','registration_code')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
  list_display=('ticket_code','registration','generated_at')
  search_fields=('ticket_code',)