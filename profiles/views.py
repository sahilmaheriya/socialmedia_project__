from django.contrib.auth import login
from django.contrib.auth.models import User
# from django.dispatch.dispatcher import receiver
from django.shortcuts import redirect, render, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url='login')
def my_profile(request):
    profile = Profile.objects.get(user = request.user)
    confirm = False
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    return render(request, 'profiles/myprofile.html', {'profile':profile,'form':form, 'confirm':confirm})

@login_required(login_url='login')
def invites_received_views(request):
    profile = Profile.objects.get(user = request.user)
    qs = Relationship.objects.invitation_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    return render(request, 'profiles/my_invites.html', {'qs':results, 'is_empty':is_empty})

@login_required(login_url='login')
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    return render(request, 'profiles/profile_list.html', {'qs':qs}) 

@login_required(login_url='login')
def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk = pk)
        receiver = Profile.objects.get(user = request.user)
        rel = get_object_or_404(Relationship, sender = sender, receiver = receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('my-invites-view')

@login_required(login_url='login')
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk = pk)
        receiver = Profile.objects.get(user = request.user)
        rel = get_object_or_404(Relationship, sender = sender, receiver = receiver)
        rel.delete()
    return redirect('my-invites-view')



class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self, slug = None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug = slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact = self.request.user)
        profile = Profile.objects.get(user = user)
        rel_r = Relationship.objects.filter(sender = profile)
        rel_s = Relationship.objects.filter(receiver = profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_author_posts()
        context['len_posts'] = True if len(self.get_object().get_all_author_posts()) > 0 else False
        return context    


class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact = self.request.user)
        profile = Profile.objects.get(user = user)
        rel_r = Relationship.objects.filter(sender = profile)
        rel_s = Relationship.objects.filter(receiver = profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context
    
@login_required(login_url='login')
def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user = user)
        receiver = Profile.objects.get(pk = pk)

        rel = Relationship.objects.create(sender = sender, receiver = receiver, status = 'send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my_profile')

def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user = user)
        receiver = Profile.objects.get(pk = pk)

        rel = Relationship.objects.get(
            (Q(sender = sender) & Q(receiver = receiver)) | (Q(sender = receiver) & Q(receiver = sender)))
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my_profile')

def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    return render(request, 'profiles/to_invite_list.html', {'qs':qs})