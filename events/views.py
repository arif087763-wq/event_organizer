# events/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, EventRegistration
from payment.forms import PaymentProofForm
from payment.models import Payment
from django.http import HttpResponseForbidden

def event_list(request):
    events = Event.objects.filter(is_published=True)
    return render(request, "events/event_list.html", {"events": events})

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    user_registration = None
    if request.user.is_authenticated:
        user_registration = EventRegistration.objects.filter(
            event=event,
            participant=request.user
        ).first()

    return render(request, "events/event_detail.html", {
        "event": event,
        "user_registration": user_registration,
    })

@login_required
def event_register(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    registration, created = EventRegistration.objects.get_or_create(
        event=event,
        participant=request.user,
    )
    return redirect("events:event_detail", slug=event.slug)

@login_required
def event_dashboard_participant(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    registration = EventRegistration.objects.filter(
        event=event,
        participant=request.user
    ).first()
    return render(request, "events/event_dashboard_participant.html", {
        "event": event,
        "registration": registration,
    })


  


@login_required
def event_payment(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    registration = get_object_or_404(
        EventRegistration,
        event=event,
        participant=request.user
    )

    if not event.is_paid():
        return redirect('events:event_detail', slug=slug)

    payment, created = Payment.objects.get_or_create(
        registration=registration,
        defaults={'amount': event.price}
    )

    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            form.save()
            # setelah upload, user menunggu konfirmasi admin
            return redirect('events:event_dashboard_participant', slug=slug)
    else:
        form = PaymentProofForm(instance=payment)

    return render(request, "events/event_payment.html", {
        "event": event,
        "registration": registration,
        "form": form,
    })
@login_required
def organizer_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("anda tidak memiliki akses ke halaman ini")
    events=Event.objects.filter(organizer=request.user)
    if request.user.is_superuser:
        events_qs=Event.objects.all()
    else:
        events_qs=Event.objects.filter(organizer=request.user)
    
    events_stats=[]
    for event in events_qs:
        total_reg=event.registrations.count()  
        paid_reg=event.registrations.filter(status='paid').count()
        total_income=event.registrations.filter(status='paid').count() * float(event.price)

        events_stats.append({
            "event":event,
            "total_reg":total_reg,
            "paid_reg":paid_reg,
            "total_income":total_income
        })
    context={
        "event_stats":events_stats,
    }

    return render(request,"events/organizer_dashboard.html",context)

@login_required
def organizer_event_detail(request,slug):
    if not request.user.is_staff:
        return HttpResponseForbidden("anda tidak memiliki akses ke halaman ini.")
    
    event=get_object_or_404(Event,slug=slug)
    if not request.user.is_superuser and event.organizer != request.user:
        return HttpResponseForbidden("anda tidak boleh melihat event ini")
    registration=event.registrations.select_related('participant').all()

    context={
        "event":event,
        "registrations":registration,
    }
    return render(request,"events/organizer_event_detail.html",context)
