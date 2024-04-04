from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.views import View
from django.urls import reverse_lazy
from .models import blogPost, postComment
# Create your views here.

class postCommentDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args,**kwargs):
        comment = get_object_or_404(postComment, pk=kwargs['pk'])
        post_pk = comment.post.id
        comment.delete()
        return HttpResponseRedirect(reverse_lazy('post-detail', kwargs={'pk': post_pk}))

class CustomRegisterPage(FormView):
    template_name = 'blogApp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('post-list')

    def form_valid(self, form: Any) -> HttpResponse:
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(CustomRegisterPage, self).form_valid(form)

    def get(self, *arg, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('post-list')
        return super(CustomRegisterPage, self).get(*arg, **kwargs)


def CustomLogoutView(request):
    logout(request)
    return redirect('post-list')


class CustomLoginView(LoginView):
    template_name = 'blogApp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy('post-list')


class postListView(ListView):
    model = blogPost
    template_name = 'blogApp/post_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ''

        if search_input:
            context['posts'] = context['posts'].filter(
                title__startswith=search_input)
        context['search_input'] = search_input
        return context


class postDetailView(LoginRequiredMixin, DetailView):
    model = blogPost
    template_name = 'blogApp/post_detail.html'
    context_object_name = 'post'
    success_url = 'post-detail'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        print(post)
        context['is_user_liked'] = self.request.user in self.object.likes.all()
        context['comments'] = postComment.objects.filter(post=post)
        # context['likes'] = self.object.likes.count()
        context['likes'] = post.like_count()
        return context

    def post(self, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        text = self.request.POST['comment-area']
        comment = postComment.objects.create(post = post, user = user, text = text)
        return redirect('post-detail', post.id)

class postCreateView(LoginRequiredMixin, CreateView):
    model = blogPost
    template_name = 'blogApp/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('post-list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = self.request.user
        return super(postCreateView, self).form_valid(form)


class postUpdateView(LoginRequiredMixin, UpdateView):
    model = blogPost
    template_name = 'blogApp/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('post-list')


class postDeleteView(LoginRequiredMixin, DeleteView):
    model = blogPost
    template_name = 'blogApp/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')


class postLikeView(View):

    def post(self, *args, **kwargs):
        post = get_object_or_404(blogPost, pk=kwargs['pk'])
        user = self.request.user
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return redirect('post-detail', pk=post.pk)

class postLikeView(View):

    def post(self, *args, **kwargs):
        post = get_object_or_404(blogPost, pk=kwargs['pk'])
        user = self.request.user
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return redirect('post-detail', pk=post.pk)