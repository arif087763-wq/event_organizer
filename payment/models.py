# payments/models.py
from django.db import models
from django.utils import timezone
from django.core.files.base import ContentFile
from io import BytesIO
import uuid
import qrcode

from events.models import EventRegistration, Ticket


class Payment(models.Model):
    METHOD_CHOICES = (
        ('manual_transfer', 'Manual Bank Transfer'),
        ('gateway_dummy', 'Dummy Gateway'),
    )

    registration = models.OneToOneField(EventRegistration, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES, default='manual_transfer')
    is_confirmed = models.BooleanField(default=False)
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_confirmed_before = False
        if self.pk:
            old = Payment.objects.get(pk=self.pk)
            is_confirmed_before = old.is_confirmed

        super().save(*args, **kwargs)

        if not is_confirmed_before and self.is_confirmed:
            self.confirmed_at = timezone.now()
            super().save(update_fields=['confirmed_at'])

            reg = self.registration
            reg.status = 'paid'
            reg.save()

            if not hasattr(reg, 'ticket'):
                ticket_code = str(uuid.uuid4()).replace('-', '').upper()[:10]
                qr = qrcode.make(ticket_code)
                buffer = BytesIO()
                qr.save(buffer, format='PNG')
                filename = f"ticket_{ticket_code}.png"

                ticket = Ticket.objects.create(
                    registration=reg,
                    ticket_code=ticket_code
                )
                ticket.qr_image.save(filename, ContentFile(buffer.getvalue()), save=True)

    def __str__(self):
        return f"Payment for {self.registration}"
