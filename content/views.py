from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Post, User
from .filters import PostFilter
from .forms import NewsForm, ProfileEditForm, PasswordEditForm, UserRegisterForm


class NewsListView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-time_in'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        number_of_posts = Post.objects.aggregate(total_news=Count('id'))
        user = self.request.user
        context['is_author'] = user.groups.filter(name='author').exists()
        context['number_of_posts'] = number_of_posts.get('total_news')
        return context


class NewsDetailView(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = "obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        context['is_author'] = user.groups.filter(name='author').exists()
        return context


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
    form_class = NewsForm
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


class ArticleCreateView(CreateView):
    form_class = NewsForm
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


class NewsEditView(UpdateView):
    form_class = NewsForm
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
    success_url = reverse_lazy('news_search')


class ProfileView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
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
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect(to='profile')

