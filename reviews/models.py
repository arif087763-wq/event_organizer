from django.db import models
from django.conf import settings
from events.models import Event


class EventReview(models.Model):
  event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='reviews')
  user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='event_reviews')
  rating=models.PositiveSmallIntegerField()
  comment=models.TextField()
  created_at=models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('event','user')

  def __str__(self):
    return f"Review {self.event.title} by {self.user.username}"