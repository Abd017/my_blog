from django import forms
from .models import BlogPost


class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)
    published_date = forms.DateTimeField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))


class BlogPostModelForm(forms.ModelForm):

    ##published_date = forms.DateTimeField(attrs={'placeholder':"YYYY-MM-DD"})

    class Meta:
        model = BlogPost
        fields = [
            'title', 'image', 'slug', 'content', 'published_date'
        ]
        widgets = {
            'published_date': forms.DateTimeInput(attrs={'placeholder':'YYYY-MM-DD HH:MM:SS'})
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
