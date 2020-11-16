from django.db import models
import datetime
from django.db.models import Q
from django.contrib.auth.models import User


class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = datetime.datetime.now()
        return self.filter(published_date__lte=now)

    def search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__username__icontains=query) |
                Q(slug__icontains=query)
        )
        return self.filter(lookup)


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search()


class BlogPost(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BlogPostManager()

    class Meta:
        ordering = ['-published_date', '-updated', '-timestamp']

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_edit_url(self):
        return f"/blog/{self.slug}/edit"

    def get_delete_url(self):
        return f"/blog/{self.slug}/delete"
