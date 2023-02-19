from django.db import models


class Comment(models.Model):
    author = models.TextField(max_length=25)
    text = models.TextField(max_length=100)
    date = models.DateField()
    id_user = models.ForeignKey("User", on_delete=models.CASCADE)
    id_post = models.ForeignKey("Post", on_delete=models.CASCADE)
