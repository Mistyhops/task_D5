from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'news/news.html'
    queryset = Post.objects.order_by('-time')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['all_news'] = Post.objects.all()

        return context


class PostSearch(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'news/post_search.html'
    queryset = Post.objects.order_by('-time')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data(**kwargs)

        post_list = PostFilter(self.request.GET, queryset=Post.objects.all()).qs
        paginator = Paginator(post_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            post_filter = paginator.page(page)
        except PageNotAnInteger:
            post_filter = paginator.page(1)
        except EmptyPage:
            post_filter = paginator.page(paginator.num_pages)

        context['all_news'] = Post.objects.all()
        context['filter'] = PostFilter(self.request.GET, queryset=super().get_queryset())
        context['post_list'] = post_filter
        context['filterset'] = post_filter

        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/specificnews.html'
    context_object_name = 'specificnews'


class PostCreate(PermissionRequiredMixin, CreateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post')


class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'
    context_object_name = 'specificnews'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'news/post_edit.html'
    context_object_name = 'specificnews'
    form_class = PostForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
