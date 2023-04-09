from datetime import datetime

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.cache import cache
from django.core.validators import ValidationError

from .models import Post, User, Subscribers, PostCategory, Category, Author
from .filters import PostFilter
from .forms import (
    NewsCreateForm,
    ProfileEditForm,
    PasswordEditForm,
    UserRegisterForm,
    NewsEditForm,
)
from .tasks import notify_subscribers


class NewsListView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        right_posts = Post.objects.all().order_by('-id')[4:6]
        newest = Post.objects.latest('time_in')
        newest_posts = Post.objects.all().order_by('-id')[1:3]
        other_posts = Post.objects.all().order_by('-id')[6:12]
        context = super().get_context_data()
        number_of_posts = Post.objects.aggregate(total_news=Count('id'))
        user = self.request.user
        context['is_author'] = user.groups.filter(name='author').exists()
        context['number_of_posts'] = number_of_posts.get('total_news')
        context['last_news'] = newest_posts
        context['newest'] = newest
        context['right_posts'] = right_posts
        context['other_posts'] = other_posts
        return context
    
    
class AllNewsList(ListView):
    model = Post
    template_name = 'all_news.html'
    context_object_name = 'news'
    paginate_by = 10
    ordering = '-time_in'


class NewsDetailView(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = "obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        post_id = self.kwargs['pk']
        category = PostCategory.objects.get(post_id=post_id).category_id
        context['is_author'] = user.groups.filter(name='author').exists()
        context['category'] = Category.objects.get(pk=category).category
        context['is_category_subscribe'] = self.check_subcriber(self.request)
        return context

    def post(self, request, *args, **kwargs):
        redir_id = self.kwargs['pk']
        if 'sub' in request.POST:
            subscriber = Subscribers(
            user=request.user,
            category=PostCategory.objects.get(
                post_id=self.kwargs['pk']
            ).category)
            subscriber.save()
        elif 'unsub' in request.POST:
            Subscribers.objects.filter(
                user = request.user,
                category = PostCategory.objects.get(
                post_id=self.kwargs['pk']
                ).category
            ).delete()
        return HttpResponseRedirect(f'{redir_id}')

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj
    
    def check_subcriber(self, request, **kwargs):
        post_id = self.kwargs['pk']
        category = PostCategory.objects.get(post_id=post_id).category_id
        res = Subscribers.objects.filter(
            user_id=self.request.user.id, category_id=category
        ).exists()
        return res



class NewsSearchView(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'news_search'
    ordering = '-time_in'
    template_name = 'news_search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreateView(CreateView):
    form_class = NewsCreateForm
    template_name = 'news_add.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'N'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        context['is_author'] = user.groups.filter(name='author').exists()
        return context

    def post(self, request, *args, **kwargs):
        post = Post(
            author=Author.objects.get(pk=request.POST['author']),
            time_in=datetime.utcnow(),
            title=request.POST['title'],
            text=request.POST['text'],
            type='A',
        )
        try:
            post.save()
            PostCategory.objects.create(
                post_id=post.id, category_id=request.POST['category']
            )
            notify_subscribers.delay(post.id)
            return redirect('news_list')
        except ValidationError:
            form = NewsCreateForm(request.POST)
            user = self.request.user
            messages.error(
                request, 'Вы не можете добавлять более 3-х постов в день!'
            )
            is_author = user.groups.filter(name='author').exists()
            return render(
                self.request,
                self.template_name,
                {'form': form, 'is_author': is_author},
            )


class ArticleCreateView(CreateView):
    form_class = NewsCreateForm
    model = Post
    template_name = 'article_add.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type = 'A'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        context['is_author'] = user.groups.filter(name='author').exists()
        return context

    def post(self, request, *args, **kwargs):
        post = Post(
            author=Author.objects.get(pk=request.POST['author']),
            time_in=datetime.datetime.utcnow(),
            title=request.POST['title'],
            text=request.POST['text'],
            type='A',
        )
        try:
            post.save()
            PostCategory.objects.create(
                post_id=post.id, category_id=request.POST['category']
            )
            notify_subscribers.delay(post.id)
            return redirect('news_list')
        except ValidationError:
            form = NewsCreateForm(request.POST)
            user = self.request.user
            is_author = user.groups.filter(name='author').exists()
            return render(
                self.request,
                self.template_name,
                {'form': form, 'is_author': is_author},
            )


class NewsEditView(UpdateView):
    form_class = NewsEditForm
    model = Post
    template_name = 'news_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        context['is_author'] = user.groups.filter(name='author').exists()
        return context


class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ProfileView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['is_author'] = self.request.user.groups.filter(
            name='author'
        ).exists()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = ProfileEditForm
    template_name = 'profile/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


class PasswordEditView(LoginRequiredMixin, PasswordChangeView):
    model = User
    form_class = PasswordEditForm
    template_name = 'profile/password_change.html'
    success_url = reverse_lazy('profile')


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = 'news_list'
    template_name = 'sign/signup.html'


@login_required()
def get_author(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect(to='profile')


class SelfEducationView(View):
    template_name = 'test.html'

    def get(self, request):
        return render(request, 'test.html')
