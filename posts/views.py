from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from profiles.models import Profile
from .models import Comment, Like, Post
from .forms import CommentModelForm, PostModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required(login_url='login')
def post_comment_create_and_list_view(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user = request.user)
    
    post_form = PostModelForm()
    comment_form = CommentModelForm()
    post_added = False

    if 'submit_p_form' in request.POST:
        post_form = PostModelForm(request.POST or None, request.FILES or None)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_added = True
            post_form = PostModelForm()
    
    if 'submit_c_form' in request.POST:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id = request.POST.get('post_id'))
            instance.save()
            comment_form = CommentModelForm()
    return render(request, 'main.html', {'qs':qs, 'profile':profile, 'post_form':post_form, 'comment_form':comment_form, 'post_added':post_added})

@login_required(login_url='login')
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id = post_id)
        profile = Profile.objects.get(user = user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        
        like, created = Like.objects.get_or_create(user = profile, post_id = post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        else:
            like.value = 'Like'

            post_obj.save()
            like.save()

    return redirect('main_post_view')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    model = Post
    template_name = 'confirm_del.html'
    success_url = '/posts'

    def get_object(self , *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk = pk)
        if not obj.author.user == self.request.user:
            messages.Warning(self.request, 'You need to be author of the post in order to delete it')
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    form_class = PostModelForm
    model = Post
    template_name = 'update.html'
    success_url  = '/posts'

    def form_valid(self, form):
        profile = Profile.objects.get(user = self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You need to be author of the post in order to update it')
            return super().form_invalid(form)
        