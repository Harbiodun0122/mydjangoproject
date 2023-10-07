from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from Account.models import Account
from Account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from Blog.models import BlogPost
from Blog.views import get_blog_queryset
from operator import attrgetter


# Create your views here


def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('Account:home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'Account/register_user.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')


def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("Account:home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("Account:home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "Account/login.html", context)


def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email,
					"username": request.user.username,
				}
			)

	context['account_form'] = form

	blog_posts = BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts

	return render(request, "Account/account.html", context)


def must_authenticate_view(request):
	return render(request, 'Account/must_authenticate.html', {})

def technical_analysis(request):
	technical_analysis = BlogPost.objects.filter(category="TECHNICAL ANALYSIS")
	context = {
		'technical_analysis':technical_analysis
	}
	return render(request, 'Blog/categories/technical_analysis.html', context)

def fundamental_analysis(request):
	fundamental_analysis = BlogPost.objects.filter(category="FUNDAMENTAL ANALYSIS")
	context = {
		'fundamental_analysis':fundamental_analysis
	}
	return render(request, 'Blog/categories/fundamental_analysis.html', context)

def forex_quotes(request):
	forex_quotes = BlogPost.objects.filter(category="FOREX QUOTES")
	context = {
		'forex_quotes':forex_quotes
	}
	return render(request, 'Blog/categories/forex_quotes.html', context)




# Create your views here.

BLOG_POSTS_PER_PAGE = 10


def home_screen_view(request, *args, **kwargs):

    context = {}

    # Search
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)


    blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blog_posts'] = blog_posts

    return render(request, "Account/home.html", context)
