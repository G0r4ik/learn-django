from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateField()
    id_user = models.ForeignKey("User", on_delete=models.CASCADE)
