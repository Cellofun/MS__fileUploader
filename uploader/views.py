import os

from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import Post, Tag


class PostList(generic.ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(title__icontains=query).order_by("-created_at")
        else:
            return Post.objects.all().order_by("-created_at")


class UserPostList(generic.ListView):
    model = Post
    template_name = 'post/post_user.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-created_at")


class NewPost(generic.CreateView):
    model = Post
    template_name = 'post/post_new.html'
    fields = ('title', 'tags', 'upload')
    template_name_suffix = '_new'
    success_url = '/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostDelete(generic.DeleteView):
    model = Post
    success_url = '/'


class PostEdit(generic.UpdateView):
    model = Post
    template_name = 'post/post_edit.html'
    fields = ('title', 'tags', 'upload')
    template_name_suffix = '_update_form'
    success_url = '/'


def about(request):
    return render(request, 'uploader/about.html')


def download(request, pk):
    post = Post.objects.get(id=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, post.upload.path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


class TagList(generic.ListView):
    model = Tag
    template_name = 'tag/tag_list.html'
    context_object_name = 'tags'


class NewTag(generic.CreateView):
    model = Tag
    template_name = 'tag/tag_new.html'
    fields = '__all__'
    template_name_suffix = '_new'
    success_url = '/tags'


class TagDetail(generic.ListView):
    model = Tag
    template_name = 'tag/tag_detail.html'
    context_object_name = 'tag_posts'

    def get_queryset(self):
        queryset = Post.objects\
            .filter(tags__name__iexact=self.kwargs['tag_name'])\
            .order_by("-created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs['tag_name']
        return context


class RegisterView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)
