from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import datetime as dt

# Create your models here.


class Profile(models.Model):
    class Meta:
        db_table = 'profile'
    profile_photo = models.ImageField(upload_to='images/', blank=True)
    contact_no =  models.CharField(max_length = 10,blank =True)
    email = models.EmailField(max_length=70, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def save_profile(self):
        self.save()

    def delete_profile(cls, id):
        self.delete()

    def update_profile(self,update):
        self.bio = update
        self.save()
    @classmethod
    def get_all_profiles(cls):
        proff = cls.objects.all()
        return proff

    @classmethod
    def get_profile(cls, id):
        profile = Profile.objects.get(user=id)
        return profile

    @classmethod
    def find_profile(cls, search_term):
        profile = Profile.objects.filter(user__username__icontains=search_term)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user=id).first()
        return profile

class Neighborhood(models.Model):
    hood = models.CharField(max_length=30, default="e.g Kagarama, Niboyi, Gisenyi etc")
    location = models.CharField(max_length=30)
    occupants_count = models.IntegerField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hoods', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    police =  models.CharField(max_length = 10,blank =True)
    health_department =  models.CharField(max_length = 10,blank =True)

    def __str__(self):
        return self.hood

    @classmethod
    def search_neighborhood_by_name(cls, search_term):
        neighborhoods = cls.objects.filter(name__icontains=search_term)
        return neighborhoods

    @classmethod
    def find_neigborhood(cls, id):
        neighborhood = Neighborhood.objects.filter(id=id)
        return neighborhood

    @classmethod
    def all_neighborhoods(cls):
        neighborhoods = cls.objects.all()
        return neighborhoods

    @classmethod
    def get_all_profiles(cls):
        profile = Profile.objects.all()
        return profile


class Business(models.Model):
    name = models.CharField(max_length=30)
    description = HTMLField(blank=True)
    email = models.EmailField(max_length=70, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='biz', null=True)

    def __str__(self):
        return self.name

    @classmethod
    def search_by_name(cls, search_term):
        businesses = cls.objects.filter(name__icontains=search_term)
        return businesses
    
    @classmethod
    def find_by_neigborhood(cls, hood):
        buss = Business.objects.filter(hood=hood)
        return buss

class Post(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='pictures/', blank=True)
    description = HTMLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def save_post(self):
        self.save()

    @classmethod
    def all_posts(cls,id):
        posts = Post.objects.all()
        return posts

    @classmethod
    def search_by_name(cls, search_term):
        post = cls.objects.filter(name__icontains=search_term)
        return post

class Join(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    hood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user_id