from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostModelForm


def blog_post_list_view(request):
    # list/search out object
    qs = BlogPost.objects.all().published()
    print(qs)
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    context = {
        'object_list': qs
    }
    print(qs)
    return render(request, 'blog/list.html', context)


@login_required
def blog_post_create_view(request):
    if request.user.is_active:
        form = BlogPostModelForm(request.POST or None, request.FILES or None)
        print(form)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(blog_post_detail_view, slug=obj.slug)

    context = {
        'form': form,
        'title': "Create your blog here"
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
    form = BlogPostModelForm(data=request.POST or None, files=request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        slug = form.cleaned_data["slug"]
        return redirect(blog_post_detail_view, slug=slug)
    context = {
        'title': f"Update {obj.title}",
        'form': form,
    }
    return render(request, 'form.html', context)


# @staff_member_required
# @permission_required('BlogPost.can_publish_blog')
@login_required
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
