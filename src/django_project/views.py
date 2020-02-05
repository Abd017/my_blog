from django.shortcuts import render
from .forms import ContactForm
from blog.models import BlogPost


def home_page(request):
    my_title = "Hello there...."
    qs = BlogPost.objects.all()[:5]
    context = {"title": "Welcome to My Blog", 'blog_list': qs}
    return render(request, "home.html", context)


def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {
        'title': "Contact Us",
        "form": form
    }
    return render(request, 'form.html', context)