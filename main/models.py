from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
    count = models.IntegerField(default=0)
    image_name = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.image:
            self.image_name = self.image.name
        super().save(*args, **kwargs)

class Imageclassfication(models.Model):
    image = models.ForeignKey(ImageModel,on_delete=models.CASCADE)
    is_flooded = models.BooleanField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)