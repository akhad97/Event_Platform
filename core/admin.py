from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Participant)
admin.site.register(Organizer)
admin.site.register(Notification)
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(QRCode)