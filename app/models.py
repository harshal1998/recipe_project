from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if User.objects.filter(username=self.username).exists():
            a = User.objects.get(username = self.username)
            if a.password == self.password:
                return super().save(*args, **kwargs)
            else:
                self.password=make_password(self.password)
                return super().save(*args, **kwargs)
        else:
            self.password=make_password(self.password)
            return super().save(*args, **kwargs)

class Receipies(models.Model):
    name = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to='images')
    description = models.TextField(max_length=500,null=True)
    ingredients = models.TextField()
    recipe = models.TextField()
    added_by = models.ForeignKey('app.User',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Receipies'

    def __str__(self):
        return self.name