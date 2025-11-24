from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, EventRegistration
from .forms import PaymentProofForm
from .models import Payment  # sesuaikan nama app jika beda


@login_required
def event_payment(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    registration = get_object_or_404(
        EventRegistration,
        event=event,
        participant=request.user
    )

    if not event.is_paid():
        # kalau event gratis, tidak perlu pembayaran
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
