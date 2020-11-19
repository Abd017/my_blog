from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostModelForm


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


@login_required
def blog_post_create_view(request):
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if request.user.is_active:
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(blog_post_detail_view, slug=obj.slug)

    context = {
        'form': form,
        'title': "Create",
        'heading': "Create your blog here",
        'value': "Create"
    }
    return render(request, 'form.html', context)


@login_required
def blog_post_detail_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    context = {
        'object': obj
    }
    return render(request, 'blog/detail.html', context)


# @staff_member_required
# @permission_required('BlogPost.can_publish_blog')
@login_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    if request.user != obj.user:
        raise PermissionDenied

    form = BlogPostModelForm(data=request.POST or None, files=request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        slug = form.cleaned_data["slug"]
        return redirect(blog_post_detail_view, slug=slug)
    context = {
        'heading': f"Update {obj.title}",
        'form': form,
        'value': "Update"
    }
    return render(request, 'form.html', context)


# @staff_member_required
# @permission_required('BlogPost.can_publish_blog')
@login_required
def blog_post_delete_view(request, slug):
    if request.user.is_active:
        obj = get_object_or_404(BlogPost, slug=slug)
        if request.user != obj.user:
            raise PermissionDenied
        if request.method == "POST":
            obj.delete()
            return redirect("/blog")
    else:
        return redirect('/accounts/login/')

    context = {
        'object': obj
    }
    return render(request, 'blog/delete.html', context)
