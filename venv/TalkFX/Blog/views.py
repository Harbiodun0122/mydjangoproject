from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from Blog.models import BlogPost
from Blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from Account.models import Account

# Create your views here.



def create_blog_view(request):
	'''This function handles the creation of a blog'''
	user = request.user
	if not user.is_authenticated:
		return redirect('Account:must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		return redirect("Account:home")

	context = {
		'form': form
	}

	return render(request, "Blog/create_blog.html", context)


def detail_blog_view(request, slug):
	''' This will show the all details about the blog'''

	blog_post = get_object_or_404(BlogPost, slug=slug)

	context = {
		'blog_post':blog_post
	}

	return render(request, 'Blog/detail_blog.html', context)



def edit_blog_view(request, slug):
	''' Handles the editing of blogpost'''

	user = request.user
	if not user.is_authenticated:
		return redirect("Account:must_authenticate")

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse('Sorry, only the author of the post can edit the post.')

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			blog_post = obj
			return redirect('Account:home')

	form = UpdateBlogPostForm(
			initial = {
					"title": blog_post.title,
					"body": blog_post.body,
					"image": blog_post.image,
			}
		)

	context = {
		'form': form
	}

	return render(request, 'Blog/edit_blog.html', context)

def delete_blog_view(request, slug):
	''' This function handles the deleting of blogposts'''

	user = request.user
	if not user.is_authenticated:
		return redirect("Account:must_authenticate")

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse('Sorry, only the author of the post can delete the post.')

	if request.method == 'POST':
		blog_post.delete()
		return redirect('Account:home')

	context = {

	}
	return render(request, 'Blog/delete_blog.html', context)


def get_blog_queryset(query=None):
	''' This function collects the input(title o body) from the user  and displays the result if any'''

	queryset = []
	queries = query.split(" ") # python install 2019 = [python, install, 2019]
	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) |
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))
