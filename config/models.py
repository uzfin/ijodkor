from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from datetime import datetime, timedelta


class CustomUser(AbstractUser):
    user_type_data = (
        ('ADMIN', 'ADMIN'),
        ('MANAGER', 'MANAGER'),
        ("USER", 'USER')
        )
    user_type = models.CharField(default="ADMIN", choices=user_type_data, max_length=10)
    profil_pic = models.ImageField(upload_to="IMAGE/PROFILE_IMAGES", default='default.jpeg')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    @property
    def imageURL(self):
        try:
            url = self.profil_pic.url
        except:
            url=''
        return url


class Managers(models.Model):
    manager = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Managers"

    def __str__(self):
        return self.manager.username

class TalandCategory(models.Model):
    name=models.CharField(max_length=100)
    whofrom = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def user_type_name(self):
        return self.whofrom.user_type
    
    class Meta:
        verbose_name_plural = "Category"


class Artists(models.Model):
    artist=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    taland_category=models.ManyToManyField(TalandCategory, related_name='categories', blank=True)
    phone_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Talant"
    
    def __str__(self):
        return self.artist.username

class LikeID(models.Model):
    like_name = models.CharField(max_length=100)

    def __str__(self):
        return self.like_name

class UnLikeID(models.Model):
    un_like_name = models.CharField(max_length=100)

    def __str__(self):
        return self.un_like_name

class Sher(models.Model):
    SITUATION = {
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    }
    user = models.ForeignKey(Artists, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = RichTextUploadingField(null=True)
    situation = models.CharField(max_length=50, choices=SITUATION, null=True, default='Active')
    like = models.ManyToManyField(LikeID, blank=True, related_name='like_set')
    unlike = models.ManyToManyField(UnLikeID, blank=True, related_name='unlike_set')
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.like.count()
    
    def total_unlikes(self):
        return self.unlike.count()
    





class Rassom(models.Model):
    SITUATION = {
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    }
    user = models.ForeignKey(Artists, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)
    situation = models.CharField(max_length=50, choices=SITUATION, null=True, default='Inactive')
    img=models.ImageField(upload_to='IMAGE/images')
    deleted = models.BooleanField(default=False)
    like = models.ManyToManyField(LikeID, blank=True)
    unlike = models.ManyToManyField(UnLikeID, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.like.count()
    
    def total_unlikes(self):
        return self.unlike.count()

    def __str__(self):
        return self.title
    
    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url=''
        return url


class Image(models.Model):
    rassom = models.ForeignKey(
        Rassom, on_delete=models.CASCADE, null=True
        )
    image = models.ImageField(blank=True, upload_to='IMAGE/images')

    def __str__(self):
        return self.rassom.title
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url


class Videos(models.Model):
    SITUATION = {
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    }
    user = models.ForeignKey(Artists, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)
    situation = models.CharField(max_length=50, choices=SITUATION, null=True, default='Inactive')
    videofile = models.FileField(upload_to='VIDEOS/videos/', null=True, verbose_name="")
    deleted = models.BooleanField(default=False)
    like = models.ManyToManyField(LikeID, blank=True)
    unlike = models.ManyToManyField(UnLikeID, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.like.count()
    
    def total_unlikes(self):
        return self.unlike.count()
    
class Song(models.Model):
    SITUATION = {
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    }
    user = models.ForeignKey(Artists, on_delete=models.CASCADE, null=True)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='', upload_to="SONG/song")
    situation = models.CharField(max_length=50, choices=SITUATION, null=True, default='Inactive')
    deleted = models.BooleanField(default=False)
    like = models.ManyToManyField(LikeID, blank=True)
    unlike = models.ManyToManyField(UnLikeID, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.song_title
    
    @property
    def total_likes(self):
        return self.like.count()
    
    def total_unlikes(self):
        return self.unlike.count()


# -=-=-=-=-=-=-=-==--=-=-=--==--=-=--=-=-=-==---=-=-= COMPETITIO -==--=--=-=-=-=-=-=-=-=--=---=--=-=-==-=-=--=
class Counter(models.Model): 
    COMPETITION = {
        ('Music', 'Music'),
        ('Painting', 'Painting'),
        ('Writer', 'Writer'),
        ('Video', 'Video'),
    }
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    competition = models.CharField(max_length=50, choices=COMPETITION, null=True, default='Music')

    def __str__(self):
        return str(self.year)
    
class Phone_numbers(models.Model):
    phone_number = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.phone_number
    
class SmsPhoneVerify(models.Model):
    code = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    publishing_date = models.DateTimeField(
    auto_now_add=True,
    blank=True,
    )

    def __str__(self):
        return self.code

# ---------------------------------------- ---------------------------------- --------------------------------   
class Comp_Song(models.Model):
    SITUATION = {
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    }
    user = models.ForeignKey(Artists, on_delete=models.CASCADE, null=True)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='', upload_to="SONG/song")
    situation = models.CharField(max_length=50, choices=SITUATION, null=True, default='Inactive')
    deleted = models.BooleanField(default=False)
    votes = models.ManyToManyField(Phone_numbers, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# ---------------------------------------- ---------------------------------- --------------------------------   

class Comp_Video(models.Model):
    SITUATION = {
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    }
    user = models.ForeignKey(Artists, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)
    videofile = models.FileField(upload_to='COMPETITION/videos/', null=True, verbose_name="")
    situation = models.CharField(max_length=50, choices=SITUATION, null=True, default='Inactive')
    deleted = models.BooleanField(default=False)
    votes = models.ManyToManyField(Phone_numbers, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comp_Sher(models.Model):
    SITUATION = {
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    }
    user = models.ForeignKey(Artists, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = RichTextUploadingField(null=True)
    situation = models.CharField(max_length=50, choices=SITUATION, null=True, default='Active')
    votes = models.ManyToManyField(Phone_numbers, blank=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    

class Comp_Rassom(models.Model):
    SITUATION = {
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    }
    user = models.ForeignKey(Artists, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)
    situation = models.CharField(max_length=50, choices=SITUATION, null=True, default='Inactive')
    img=models.ImageField(upload_to='IMAGE/images')
    deleted = models.BooleanField(default=False)
    votes = models.ManyToManyField(Phone_numbers, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    

class Comp_Image(models.Model):
    rassom = models.ForeignKey(
        Comp_Rassom, on_delete=models.CASCADE, null=True
        )
    image = models.ImageField(blank=True, upload_to='IMAGE/comp_images')

    def __str__(self):
        return self.rassom.title
    