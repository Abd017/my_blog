from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import BlogPost
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import BlogPostForm, BlogPostModelForm


def blog_post_list_view(request):
    # list/search out object
    qs = BlogPost.objects.all().published()
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    context = {
        'object_list': qs
    }
    return render(request, 'blog/list.html', context)


# @staff_member_required
def blog_post_create_view(request):
    if request.user.is_active:
        form = BlogPostModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            form = BlogPostModelForm()
            return redirect(blog_post_detail_view, slug=obj.slug)
    else:
        return redirect('/accounts/login/')

    context = {
        'form': form,
        'title': "Create your blog here"
    }
    return render(request, 'form.html', context)


def blog_post_detail_view(request, slug):

    obj = get_object_or_404(BlogPost, slug=slug)
    context = {
        'object': obj
    }
    return render(request, 'blog/detail.html', context)


#@staff_member_required
#@permission_required('BlogPost.can_publish_blog')
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        sl = form.cleaned_data["slug"]
        return redirect(blog_post_detail_view,slug=sl)
    context = {
        'title': f"Update {obj.title}",
        'form': form,
    }
    return render(request, 'form.html', context)


# @staff_member_required
#@permission_required('BlogPost.can_publish_blog')
def blog_post_delete_view(request, slug):
    if request.user.is_active:
        obj = get_object_or_404(BlogPost, slug=slug)
        if request.method == "POST":
            obj.delete()
            return redirect("/blog")
    else:
        return redirect('/accounts/login/')

    context = {
        'object': obj
    }
    return render(request, 'blog/delete.html', context)


def register(request):
    if request.method =="POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/blog')
    else:
        form = UserCreationForm()
    context={
        'form': form
    }
    return render(request, 'registration/register.html', context)

def logout_view(request):
    logout(request)
    return redirect("/")