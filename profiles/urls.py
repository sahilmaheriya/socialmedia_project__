from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileListView.as_view(), name="all-profiles-view"),
    path('myprofile/', views.my_profile, name="my_profile"),
    path('my-invites/', views.invites_received_views, name="my-invites-view"),
    path('to-invite/', views.invite_profiles_list_view, name="invite-profiles-view"),
    path('send-invite/', views.send_invitation, name="send-invite"),
    path('remove-friend/', views.remove_from_friends, name="remove-friend"),
    path('<slug>/', views.ProfileDetailView.as_view(), name="profile-detail-view"),
    path('my-invites/accept/', views.accept_invitation, name="accept-invite"),
    path('my-invites/reject/', views.reject_invitation, name="reject-invite"),
]
