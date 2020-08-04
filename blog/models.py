from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Category(models.Model):
	category = models.CharField(max_length=100)
	class Meta:
		verbose_name_plural = "Categories"
	def __str__(self):
		return self.category

class Post(models.Model):
	
	title = models.CharField(max_length=100)
	content = RichTextUploadingField(blank=True, null=True)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)#on_delete deltes post if user is deleted
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	favourite = models.ManyToManyField(User, related_name = 'favourite', blank=True)
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail',kwargs={'pk': self.pk})
    



    	

