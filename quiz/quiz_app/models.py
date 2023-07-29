from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,username,password=None,**extra_fields):
        if username is None:
            raise ValueError("Username is required")
        username=self.normalize_email(username)
        user=self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(username,password,**extra_fields)
class CustomUser(AbstractUser,PermissionsMixin):
    name=models.CharField(max_length=100,null=True,blank=True)
    email=models.EmailField(null=True,blank=True,unique=True)
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()
class Question(models.Model):
    question=models.CharField(max_length=300,null=True,blank=True)
    answer=models.TextField(max_length=100,null=True,blank=True)
    
    
    def __str__(self):
        return self.question
class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,null=True,blank=True,related_name='answers')
    option1=models.CharField(max_length=100,null=True,blank=True)
    option2=models.CharField(max_length=100,null=True,blank=True)
    option3=models.CharField(max_length=100,null=True,blank=True)
    option4=models.CharField(max_length=100,null=True,blank=True)
class Response(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    question=models.ForeignKey(Question,on_delete=models.CASCADE,null=True,blank=True)
    user_response=models.CharField(max_length=100,null=True,blank=True)
    score=models.IntegerField(default=0,null=True,blank=True)
    status=models.CharField(max_length=150,null=True,blank=True)
    
    def __str__(self):
        return f"Response for {self.question} by {self.user}"