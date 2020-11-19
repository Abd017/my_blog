from django.utils import timezone
from django import forms
from .models import BlogPost


class BlogPostModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlogPostModelForm, self).__init__(*args, **kwargs)
        if self.instance.published_date is not None and self.instance.published_date < timezone.localtime(timezone.now()):
            del self.fields['published_date']

    class Meta:
        model = BlogPost
        fields = [
            'title', 'image', 'slug', 'content', 'published_date'
        ]
        widgets = {
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'value': 'published_date'},
                                                  format='%Y-%m-%d %H:%M:%S'),
        }

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = BlogPost.objects.filter(title__iexact=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("Title has already been used. Please try new title.")
        return title
