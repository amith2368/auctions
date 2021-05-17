from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

STATUS_CHOICE = (
    ( "active", "Active" ),
    ( "inactive", "Inactive" ),
    ( "sold", "Sold")
)

class User(AbstractUser):
       
     def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    category_type = models.CharField(max_length=36)

    def __str__(self):
        return f"{self.category_type}"


class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=100)
    image = models.URLField()
    start_bid = models.IntegerField()
    top_bid = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    status = models.CharField(max_length=20, choices = STATUS_CHOICE, default = "inactive" )
    creater = models.ForeignKey(settings.AUTH_USER_MODEL, 
                        default = 1, 
                        null = True,  
                        on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    wl = models.ManyToManyField(User, related_name = "watchlist", blank = True ) 

    def __str__(self):
        return f"{self.id}:{self.name}"

class CommentSection(models.Model):
    listing = models.ForeignKey(Listing ,on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(settings.AUTH_USER_MODEL, 
                        default = 1, 
                        null = True,  
                        on_delete = models.SET_NULL)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Bid(models.Model):
    listing = models.ForeignKey(Listing , on_delete=models.CASCADE,related_name='bids')
    user_bid = models.IntegerField()
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, 
                        default = 1, 
                        null = True,  
                        on_delete = models.SET_NULL)
    
    def __str__(self):
        return f"{self.bidder} bid { self.user_bid } for {self.listing}"
    
class Auction(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    stop = models.BooleanField(default=False)
    winner = models.ForeignKey(Bid, on_delete=models.CASCADE )

    def __str__(self):
        return f"{self.listing } sold for { self.winner }"




    
