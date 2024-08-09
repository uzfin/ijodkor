from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('',include('config.urls')),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout_user, name='logout'),
    path('doLogin', views.doLogin, name='do_login'),
    path("Admn/", include('config.admn_urls')),
    path("Manager/", include('config.manager_urls')),
    path("Talant/", include('config.talant_urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
