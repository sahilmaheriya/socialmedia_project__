from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from . import views
from socialmedia_project.settings import MEDIA_ROOT, STATICFILES_DIRS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name="home"),
    path('signup/', views.signup_user, name="signup"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('profiles/', include('profiles.urls')),
    path('posts/', include('posts.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root = STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root = MEDIA_ROOT)
