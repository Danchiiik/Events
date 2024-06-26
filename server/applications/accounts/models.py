from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.create_act_code()
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return str(self.email)
    
    def create_act_code(self):
        import uuid
        self.activation_code = str(uuid.uuid4())
        
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profiles')
    avatar = models.ImageField(null=True, blank=True, upload_to='images/avatar/')
    username = models.CharField(max_length=100)
    description = models.CharField(max_length=1500, null=True, blank=True)
    url = models.URLField(max_length=250, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = 'User' + str(self.user.id)
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f'{self.username} - {str(self.user.email)}'
        
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'