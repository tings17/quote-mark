from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    book_name = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    number_of_annotations = models.IntegerField(default=0)

    def __str__(self):
        return self.book_name
    
    class Meta:
        unique_together = ["book_name", "author_name", "user"]

class Annotation(models.Model):
    annotation_type = models.TextField(blank=True)
    image = models.ImageField(upload_to="uploaded_images/")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='annotations')
    page_number = models.IntegerField(blank=True)
    image_text = models.TextField(blank=True)
    annotation_text = models.TextField(blank=True)

    def __str__(self):
        return self.image_text
    