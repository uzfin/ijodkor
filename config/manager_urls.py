from django.urls import path
from config import manager_views
from django.conf import settings
from django.conf.urls.static import static
from .manager_views import RassomList, TalantListView

urlpatterns = [
    path('home', manager_views.manager_home, name='manager_home'),

# ================================= SHER ===========================================
    path('view_sher', manager_views.VIEW_SHER, name='view_sher_manager'),
    path("each_view_sher/<int:pk>/", manager_views.SherDetailView, name="each_view_sher_manager"),
    path('active_sher/<int:pk>', manager_views.Active_Sher, name='active_sher_manager'),
    path('inactive_sher/<int:pk>', manager_views.InActive_Sher, name='inactive_sher_manager'),

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================= SONG ===========================================
    path('list_song', manager_views.LIST_SONGS, name='list_song_manager'),
    path('active_song/<int:pk>', manager_views.Active_Song, name='active_song'),
    path('inactive_song/<int:pk>', manager_views.InActive_Song, name='inactive_song'),
    path("each_view_song/<int:pk>/", manager_views.SongDetailView, name="each_view_song_manager"),


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================= VIDEO ==========================================
    path('list_video', manager_views.LIST_VIDEOS, name='list_video_manager'),
    path('active_video/<int:pk>', manager_views.Active_Video, name='active_video'),
    path('inactive_video/<int:pk>', manager_views.InActive_Video, name='inactive_video'),
    path("each_view_video/<int:pk>/", manager_views.VideoDetailView, name="each_view_video_manager"),
   

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================= RASSOM =========================================
    path('rassoms/', RassomList.as_view(), name='list_rassoms_manager'),
    path('active_rassom/<int:pk>', manager_views.Active_Rassom, name='active_rassom'),
    path('inactive_rassom/<int:pk>', manager_views.InActive_Rassom, name='inactive_rassom'),
    path("each_view_rassom/<int:pk>/", manager_views.RassomDetailView, name="each_view_rassom_manager"),

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    path("talant/lists", TalantListView.as_view(), name="artist_lists"),
    path("talant/detail/<int:pk>/", manager_views.TalantDetailView, name="talantdetail"),
    path('talant/delete/<int:pk>', manager_views.DeleteTalant, name='delete_artist'),
    path('active_user/<int:pk>', manager_views.Active_User, name='active_artist'),
    path('inactive_user/<int:pk>', manager_views.Inactive_User, name='inactive_artist'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)