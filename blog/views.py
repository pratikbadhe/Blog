from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from django.contrib import messages
import os


# def home(request):
# 	context = {
# 	    'posts': Post.objects.all()
# 	}
# 	if request.user.is_authenticated:
# 		return render(request, 'blog/home.html', context)
# 	else:
# 		return render(request, os.path.join(PROJECT_ROOT,'users/templates/users/login.html'))

class PostListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted'] 
	paginate_by = 2     

class UserPostListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 1  
	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author = user).order_by('-date_posted')

class PostCategoryView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'blog/category_posts.html'
	context_object_name = 'posts'
	paginate_by = 1  
	def get_queryset(self):
		category = get_object_or_404(Category, category=self.kwargs.get('category'))
		return Post.objects.filter(category = category).order_by('-date_posted')

class PostDetailView(LoginRequiredMixin,DetailView):
	model = Post# it will require file with name <app>/<model>_<viewtype>.html
	def get_content_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		category = self.kwargs.get('category')
		context['post_list'] = Post.objects.all()
		return context

class PostDetailSidebarView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'blog/detail_side.html'
	context_object_name = 'posts'

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title','content','category']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title','content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class SearchView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'blog/search.html'
	context_object_name = 'posts'
	def get_queryset(self):
		result = super(SearchView, self).get_queryset()
		query= self.request.GET.get('search')
		if len(query)>50:
			search_result = Post.objects.none()
		else:
			search_result_title = Post.objects.filter(title__icontains = query)
			search_result_content = Post.objects.filter(content__icontains = query)
			search_result = search_result_title.union(search_result_content)
			search_result = search_result.order_by('title')
		# if search_result.count() == 0:
		# 	self.request.messages.error("not found")

		return (search_result)



def about(request):
	return render(request, 'blog/about.html', {'title':'About'})
