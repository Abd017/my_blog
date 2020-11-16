from django.urls import path
from .views import blog_post_detail_view, blog_post_list_view, blog_post_create_view, blog_post_delete_view, blog_post_update_view

urlpatterns = [

    path('', blog_post_list_view, name='view_all_blog_post'),
    path('new/', blog_post_create_view, name='create_blog_post'),
    path('<str:slug>/', blog_post_detail_view, name='detail_blog_post'),
    path('<str:slug>/edit/', blog_post_update_view, name='update_blog_post'),
    path('<str:slug>/delete/', blog_post_delete_view, name='delete_blog_post'),

]