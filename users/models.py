from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .manager import CustomUserManager


class UserRole(models.TextChoices):
    GOLD = 'gold', 'Gold'
    SILVER = 'silver', 'Silver'
    BRONZE = 'bronze', 'Bronze'
    NORMAL = 'normal', 'Normal'


class TaskStatus(models.TextChoices):
    OPEN = 'open', 'Open'
    REVIEW = 'review', 'Review'
    PROGRESS = 'awaiting_release', 'Awaiting Release'
    QA = 'waiting_qa', 'Waiting QA'


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    last_login = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(
        max_length=11, unique=True, blank=True, null=True
        )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_prem(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user_bio = models.CharField(max_length=50, blank=True, null=True)
    user_img = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True,
        default='default.jpg'
        )
    status = models.CharField(
        max_length=10, choices=UserRole.choices, default=UserRole.GOLD
        )
    count = models.IntegerField(default=0)
    last_hit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Project(models.Model):

    title = models.CharField(max_length=20, blank=False)
    description = models.TextField(max_length=500, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    team_member = models.ManyToManyField(CustomUser, related_name="projects")

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=20, blank=False)
    description = models.TextField(max_length=500, blank=True)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.OPEN,
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey(
        Profile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="tasks")

    def __str__(self):
        return self.title

    @property
    def get_comments(self):
        return self.comments.all()


class Document(models.Model):
    name = models.CharField(max_length=10, blank=False)
    description = models.TextField(max_length=500, blank=True)
    file = models.FileField(upload_to='documents/')
    version = models.FloatField(default=1.0)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="documents")

    def __str__(self):
        return f"{self.name} (v{self.version})"


class Comment(models.Model):
    text = models.TextField(max_length=500, blank=False, null=True)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.task.title}"
