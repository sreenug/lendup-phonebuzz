from django.db import models

class IVRCall(models.Model):
    phone_number = models.CharField(max_length=15)
    digit_entered = models.IntegerField(null=True, blank=True)
    time_delay = models.IntegerField(null=True, blank=True)
    call_sid = models.CharField(max_length=30, null=True, blank=True)
    call_time = models.DateTimeField(auto_now_add=True)