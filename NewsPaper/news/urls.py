from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostDelete, PostUpdate, PostSearch


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view()),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/delete/', PostDelete.as_view()),
    path('<int:pk>/edit/', PostUpdate.as_view()),
    path('search/', PostSearch.as_view(), name='post_search'),
]
