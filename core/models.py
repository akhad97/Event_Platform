from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser
from django.shortcuts import reverse
from cloudinary.models import CloudinaryField
from datetime import date, datetime, timedelta, time
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.http import HttpResponse
from django.db.models.signals import post_save
from django.dispatch import receiver



GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

EDUCATION = (
    ('Westminster', 'Westminster'),
    ('Inha', 'Inha'),
    ('MDIS', 'MDIS'),
    ('Turn', 'Turn'),
    ('Webster', 'Webster')
)

USER_TYPE = (
    ('Organizer', 'Organizer'),
    ('Participant', 'Participant')
)
  


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    organization = models.CharField(choices=EDUCATION, max_length=100)
    gender = models.CharField(max_length=50, choices=GENDER)
    date_of_birth = models.DateField(null=True)
    photo = models.ImageField()
    is_participant = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)
    fcm_token=models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username



# class Chat(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField()
#     posted_at = models.DateTimeField(auto_now=True)


#     def __str__(self):
#         return self.message





class Category(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    img = models.ImageField()
    num_of_participant = models.IntegerField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['start_date', 'start_time']


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event:event-detail', kwargs={'pk': self.pk})




class Comment(models.Model):
    comment = models.TextField(max_length=500)
    created_date = models.DateField(auto_now=True)
    created_time = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_date', 'created_time')

    def get_abosulte_url(self):
        return reverse('comments:comment-datail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.owner.username



class Organizer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    fcm_token=models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.user.full_name


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fcm_token=models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.full_name


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def get_absolute_url(self):
        return reverse('userprofile: detail', kwargs={'pk': self.pk})
    


class QRCode(models.Model):
    participant = models.ForeignKey(
        User, related_name="participant_qrcode", on_delete=models.CASCADE
    )
    qr_code = models.ImageField(upload_to="qr_codes")

    def str(self):
        return str(self.participant)
        
      
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.participant)
        canvas = Image.new("RGB", (290, 290), "white")
        canvas.paste(qrcode_img)
        fname = f"qr_code-{self.participant}.png"
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

        
        
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    participant_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


