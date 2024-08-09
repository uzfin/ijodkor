from django.urls import path
from config import talant_views
from django.conf import settings
from django.conf.urls.static import static

from .talant_views import (
    RassomList, RassomCreate, RassomUpdate,
    delete_image
)

urlpatterns = [
    path('home', talant_views.talant_home, name='talant_home'),

    # ========================== SHER ========================================================
    path('sher/add', talant_views.ADD_SHER, name='add_sher'),
    path('sher/view', talant_views.VIEW_SHER, name='view_sher'),
    path("sher/view/<int:pk>/", talant_views.SherDetailView, name="each_view_sher"),
    path("sher/edit/<int:pk>/", talant_views.EditSher, name="edit_sher"),
    path('sher/delete/<int:pk>', talant_views.DeleteSher, name='delete_sher'),
    # -=-=-=-=-=-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=--=-=-=-=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=

    # ========================== Rassom ======================================================
    path('rassom/view', RassomList.as_view(), name='list_rassoms'),
    path('rassom/add', RassomCreate.as_view(), name='create_rassom'),
    path('rassom/edit/<int:pk>/', RassomUpdate.as_view(), name='update_rassom'),
    path('delete-image/<int:pk>/', delete_image, name='delete_image'),
    path('rassom/delete/<int:pk>', talant_views.DeleteRassom, name='delete_rassom'),
    path("rassom/view/<int:pk>/", talant_views.RassomDetailView, name="each_view_rassom"),
    
    # -=-==-=-=-=-=-=-=-=-==--=-=-=-=-=-=-=-=-=-=--=-=--=-=-=-=--=-=--=-=-=-=-=-=--=-=-=-=-=-=

    # ========================== VIDEOS ======================================================
    path('video/add', talant_views.ADD_VIDEO, name='add_video'),
    path('video/view', talant_views.LIST_VIDEOS, name='list_video'),
    path("video/view/<int:pk>/", talant_views.VideoDetailView, name="each_view_video"),
    path('video/delete/<int:pk>', talant_views.DeleteVideo, name='delete_video'),
    path("video/edit/<int:pk>/", talant_views.EditVideo, name="edit_video"),


    # -=-==-=-=-=-=-=-=-=-==--=-=-=-=-=-=-=-=-=-=--=-=--=-=-=-=--=-=--=-=-=-=-=-=--=-=-=-=-=-=

    # ========================== SONGS =======================================================
    path('song/add', talant_views.ADD_SONG, name='add_song'),
    path('song/view', talant_views.LIST_SONGS, name='list_song'),
    path("song/view/<int:pk>/", talant_views.SongDetailView, name="each_view_song"),
    path('song/delete/<int:pk>', talant_views.DeleteSong, name='delete_song'),
    path("song/edit/<int:pk>/", talant_views.EditSong, name="edit_song"),
    # -=-==-=-=-=-=-=-=-=-==--=-=-=-=-=-=-=-=-=-=--=-=--=-=-=-=--=-=--=-=-=-=-=-=--=-=-=-=-=-=

    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)