from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )

    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    github_url = models.URLField(max_length=300, blank=True, null=True)
    website = models.URLField(max_length=300, blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, help_text="Comma-separated skills e.g. Python, React, ML")
    followers = models.ManyToManyField(
        'self', symmetrical=False,
        related_name='following', blank=True
    )

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_staff_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
