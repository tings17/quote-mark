from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    book_name = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    number_of_annotations = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.book_name
    
    class Meta:
        unique_together = ["book_name", "author_name", "user"]

class Annotation(models.Model):
    image = models.ImageField(upload_to="uploaded_images/")
    # stored in a directory within my media root directory
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='annotations')
    page_number = models.IntegerField(blank=True, null=True)
    image_text = models.TextField(blank=True)
    #book_name = models.CharField(max_length=255, blank=True)
    #author_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #annotation_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="annotations") #one to many

    # string representation method for the Annotation objects
    def __str__(self):
        # primary key
        return self.book.book_name