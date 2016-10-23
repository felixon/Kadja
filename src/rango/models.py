from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title
class UserProfile(models.Model):
	# A required line - links a UserProfile to User.
	user = models.OneToOneField(User)

	# The additional attributes we wish to include.
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):
		return self.user.username
class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'), )

    title= models.CharField(max_length=250)
    slug= models.SlugField(max_length=250,
                           unique_for_date='published')
    author = models.ForeignKey(User,
                               related_name='blog_posts')
    body = models.TextField()
    published= models.DateField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    status= models.CharField(max_length=10,
                             choices=STATUS_CHOICES,
                             default='draft')
    class Meta:
     ordering = ['published',]
    def get_absolute_url(selfs):
        return reverse('rango:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('&m'),
                             self.publish.strftime('&d'),
                             self.slug])

    def __unicode__(self):
        return self.title
class Article(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()

    def __unicode__(self):
        return self.title










