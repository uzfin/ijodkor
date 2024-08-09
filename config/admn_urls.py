from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from config import admn_views
from config.admn_views import ArtistListView, ArtistDetailView, ManagerListView, ManagerDetailView, RassomList

urlpatterns = [
    path('home', admn_views.admn_home, name='admn_home'),
    # =========================== Talant ==============================================
    path('add_talant', admn_views.ADD_TALANT, name='add_talant'),
    path("view_talant", ArtistListView.as_view(), name="view_talant"),
    path("each_view_talant/<int:pk>/", admn_views.ArtistDetailView, name="each_view_talant"),
    path('talant/<int:pk>/edit/', admn_views.EditTalant, name='talant_edit'),
    path('talant/update', admn_views.UpdateTalant, name='talant_update'),
    path('talant/delete/<int:pk>', admn_views.DeleteTalant, name='delete_talant'),
    path('active_user/<int:pk>', admn_views.Active_User, name='active_user'),
    path('inactive_user/<int:pk>', admn_views.Inactive_User, name='inactive_user'),

    # ============================ Manager ==============================================
    path('add_manager', admn_views.ADD_MANAGER, name='add_manager'),
    path("view_manager", ManagerListView.as_view(), name="view_manager"),
    path("each_view_manager/<int:pk>/", ManagerDetailView.as_view(), name="each_view_manager"),
    path('manager/<int:pk>/edit/', admn_views.ManagerEdit, name='manager_edit'),
    path('manager/update', admn_views.UpdateManager, name='manager_update'),
    path('manager/delete/<int:pk>', admn_views.DeleteManager, name='delete_manager'),
    # =-=--=-=-=----=-=-=----=-=-=-=-=-=-==-=--=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # ============================ Category ==============================================
    path('category', admn_views.CATEGORY, name='category'),
    path('category/update', admn_views.Update_category, name='update_category'),
    path('category/delete/<int:pk>', admn_views.DeleteCategory, name='delete_category'),

    # =-=--=-=-=----=-=-=----=-=-=-=-=-=-==-=--=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# ================================= SHER ===========================================
    path('sher/view', admn_views.VIEW_SHER, name='sher_list_A'),
    path("sher/view/<int:pk>/", admn_views.SherDetailView, name="each_view_sher_A"),
    path('sher/active/<int:pk>', admn_views.Active_Sher, name='active_sher_A'),
    path('sher/inactive/<int:pk>', admn_views.InActive_Sher, name='inactive_sher_A'),
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================= SONG ===========================================
    path('song/view', admn_views.LIST_SONGS, name='list_song_A'),
    path("song/view/<int:pk>/", admn_views.SongDetailView, name="each_view_song_A"),
    path('song/active/<int:pk>', admn_views.Active_Song, name='active_song_A'),
    path('song/inactive/<int:pk>', admn_views.InActive_Song, name='inactive_song_A'),
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================= VIDEO ==========================================
    path('video/view', admn_views.LIST_VIDEOS, name='list_video_A'),
    path("video/view/<int:pk>/", admn_views.VideoDetailView, name="each_view_video_A"),
    path('video/active/<int:pk>', admn_views.Active_Video, name='active_video_A'),
    path('video/inactive/<int:pk>', admn_views.InActive_Video, name='inactive_video_A'),
    
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================= RASSOM =========================================
    path('rassom/view', RassomList.as_view(), name='list_rassoms_A'),
    path("rassom/view/<int:pk>/", admn_views.RassomDetailView, name="each_view_rassom_A"),
    path('rassom/active/<int:pk>', admn_views.Active_Rassom, name='active_rassom_A'),
    path('rassom/inactivate/<int:pk>', admn_views.InActive_Rassom, name='inactive_rassom_A'),
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================ ARCHIVES =========================================
    path('archive/sher/view', admn_views.Archive_Sher, name='archive_sher_view'),
    path('archive/rassom/view', admn_views.Archive_Rassom, name='archive_rassom_view'),
    path('archive/song/view', admn_views.Archive_Song, name='archive_song_view'),
    path('archive/video/view', admn_views.Archive_Video, name='archive_video_view'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)