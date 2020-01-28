from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm


def get_posts(request):
    """
    Create a view that will return a list of posts
    that were published prior to 'now' and render them
    to the template called blogpost.html
    """
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blogpost.html', {'posts':posts})

def post_detail(request, pk):
    """
    Create a view tha return a singel post object
    based on the post id(pk) and render it to the 
    'post_detail.html' template. Or return 404
    """
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    return render(request, 'post_detail.html', {'post'=post})



def create_or_edit_a_post(request, pk=None):
    """
    Create a view that allow us to create or edit
    a post depending if the post id is null or not
    """  
    post = get_object_or_404(Post, pk=pk) if pk else None
    if request == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid:
            post = form.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blogpostform.html', {'form':form})    



