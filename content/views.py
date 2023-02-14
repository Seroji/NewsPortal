from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from .filters import PostFilter
from .forms import NewsForm, ArticleForm
from django.urls import reverse_lazy


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-time_in'
    paginate_by = 10


class NewsDetail (DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = "obj"


class NewsSearch(ListView):
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


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'N'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type = 'A'
        return super().form_valid(form)


class NewsEdit(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_search')


