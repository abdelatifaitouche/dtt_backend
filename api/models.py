from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.



class User(AbstractUser):
    username = models.CharField(max_length = 150)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  ['username',]

    def __str__(self):
        return self.username
        



class Profile(models.Model):
    user = models.OneToOneField('api.User' , on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name
    

def create_user_profile(sender , instance , created , **kwargs):
    if created : 
        Profile.objects.create(user = instance ) 

def save_user_profile(sender , instance , **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile , sender=User)
post_save.connect(save_user_profile , sender = User)





class Country(models.Model):
    country_name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.country_name

class Service(models.Model):
    title = models.CharField(max_length=100)
    country = models.ForeignKey('api.Country' , on_delete=models.CASCADE)
    max_presences = models.IntegerField()

    def __str__(self) -> str:
        return self.title



class RedevencesConditions(models.Model):
    title = models.CharField(max_length=150)
    country = models.ForeignKey('api.Country' , on_delete=models.CASCADE)
    condition = models.CharField(max_length=300)
    taux = models.FloatField()
    
    def __str__(self) -> str:
        return self.title
    


#based on the capital return a value
class DividendesConditions(models.Model):
    title = models.CharField(max_length=150)
    country = models.ForeignKey('api.Country' , on_delete=models.CASCADE)
    condition = models.CharField(max_length=300)
    taux = models.FloatField()
    
    def __str__(self) -> str:
        return self.title