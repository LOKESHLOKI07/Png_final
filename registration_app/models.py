from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import make_password

# models.py
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Company(models.Model):
    USER_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('premium', 'Premium'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, default='no-reply@example.com')
    password = models.CharField(max_length=128,null=True, blank=True)
    logo = models.ImageField(upload_to='logos/')
    banner = models.ImageField(upload_to='banners/')
    banner_content = models.TextField(null=True, blank=True)
    linkedin_url = models.URLField(max_length=200, null=True, blank=True)
    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    instagram_url = models.URLField(max_length=200, null=True, blank=True)
    twitter_url = models.URLField(max_length=200, null=True, blank=True)
    youtube_url = models.URLField(max_length=200, null=True, blank=True)
    website_url = models.URLField(max_length=200, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField()
    services = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    bullet_points = models.TextField(
        null=True,
        blank=True,
        help_text="Each new line starts with a bullet (*)."
    )
    created_by = models.CharField(max_length=255, null=True, blank=True)
    # created_at = models.DateTimeField(default=timezone.now)

    # New field for user type
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')

    def save(self, *args, **kwargs):
        if self.pk is None and self.password:  # Hash password only for new entries
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    event_img = models.ImageField(upload_to='event_img/', blank=True, null=True)
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=300)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name



class NewsUpload(models.Model):
    news_img = models.ImageField(upload_to='news_img/',blank=True,null=True)
    title = models.CharField(max_length=200)  # Title of the news article
    content = models.TextField()  # Body of the article
    publication_date = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    author = models.CharField(max_length=100)  # Optional: Author name

    def __str__(self):
        return self.title

