from django.urls import path, include
# from django.views.decorators.cache import cache_page

from .views import NewsListView, NewsDetailView, NewsSearchView, NewsCreateView, NewsEditView, NewsDeleteView, \
    ProfileView, ProfileEditView,PasswordEditView, UserRegisterView, get_author, SelfEducationView


urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>', NewsDetailView.as_view(), name='news_detail'),
    path('search/', NewsSearchView.as_view(), name='news_search'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit', NewsEditView.as_view(), name='news_edit'),
    path('<int:pk>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('sign/', include('sign.urls')),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/edit/password', PasswordEditView.as_view(), name='password_change'),
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('upgrade/', get_author, name='upgrade'),
    path('test/', SelfEducationView.as_view(), name='education')
]
