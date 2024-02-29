from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User

# Define your user_directory_path function if not already defined
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)
    # Your implementation here

RATING = (
    (1, "⭐☆☆☆☆"),
    (2, "⭐⭐☆☆☆"),
    (3, "⭐⭐⭐☆☆"),
    (4, "⭐⭐⭐⭐☆"),
    (5, "⭐⭐⭐⭐⭐"),  
)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh123456")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, default="Nepal ko Thau")
    image = models.ImageField(upload_to=user_directory_path, default="category.jpg")
    description = models.CharField( max_length=1000, null=True, blank=True, default="This category is beautiful")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        # Your implementation here
        return self.title
class Trek(models.Model):
    trek = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.CharField(max_length=50)
    trip_grade = models.CharField(max_length=50 , default='moderate')
    max_altitude = models.PositiveIntegerField()
    accommodation = models.CharField(max_length=100)
    best_travel_time = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    
    def __str__(self):
        return self.trek


class Tour(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tid = ShortUUIDField(unique=True, length=10,max_length=20, prefix="tour")
    title = models.CharField(max_length=100, default="Nepal")
    image = models.ImageField(upload_to=user_directory_path,default="tour,jpg")
    description = models.TextField(null=True, blank=True, default="This ia a beautiful place")
    short_description = models.TextField(null=True, blank= True, default="This place is an extraordinary")
    address = models.CharField(max_length=300)
    area = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(null=True, blank=True) 
    featured= models.BooleanField(default=False)  

    class Meta:
        verbose_name_plural= "Tours"
    def tour_image(self):
        return mark_safe('<img src = "%s" width="50" height="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title

    


class TourReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True, related_name="reviews") 
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Tour Reviews"
    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating

class TourImages(models.Model):
    images = models.ImageField(upload_to="tour-images", default="tour.jpg")
    tour = models.ForeignKey(Tour, related_name="t_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Tour Images" 


class TourRecommendation(models.Model):
    id = models.IntegerField(primary_key=True)
    total_review = models.IntegerField()
    review = models.TextField()
    location = models.CharField(max_length=100)
    image1 = models.ImageField(upload_to='images/')
    image2 = models.ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = "Tour Recommendations"
        