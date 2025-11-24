from django.db import models
from events.models import Event
from filer.fields.image import FilerImageField

class EventPhoto(models.Model):
  event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='photos')
  image=FilerImageField(on_delete=models.CASCADE,related_name='event_photos')
  caption=models.CharField(max_length=255,blank=True)
  uploaded_at=models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.event.title} - {self.caption or 'Photo'}"