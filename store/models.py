from django.db import models

from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField

# Create your models here.

class BaseModel(models.Model):

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


class UserProfile(BaseModel):

    bio=models.CharField(max_length=200)

    contact=models.IntegerField()

    profile_picture=models.Imagefield(upload_to='profilepictures',null=True,blank=True)

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")

    def __str__(self):

        return self.owner.username


class Tags(BaseModel):

    title=models.CharField(max_length=200)

    def __str__(self):

        return title


class Project(BaseModel):

    title=models.CharField(max_length=200)

    description=models.TextField(max_length=200)  

    preview_img=models.ImageField(upload_to="previewimages",null=True,blank=True)

    price=models.PositiveIntegerField()

    developer=models.ForeignKey(User,on_delete=models.CASCADE)

    files=models.FileField(upload_to="projects",null=True,blank=True)

    tag_obj=models.ManyToManyField(Tags,null=True) 

    thumbnail=EmbedVideoField() 


class WishList(BaseModel):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="basket")


class WishListItem(BaseModel):

    WishList_obj=models.ForeignKey(WishList,on_delete=models.CASCADE,related_name="basket-item")

    project_obj=models.ForeignKey(project,on_delete=models.CASCADE)

    is_order_placed=models.BooleanField(default=False)


class Order(BaseModel):

    wishlistitem_obj=models.ManyToManyField(WishListItem)

    is_paid=models.BooleanField(max_length=200,null=True)

    order_id=models.CharField(max_length=200,null=True)

    


        

    