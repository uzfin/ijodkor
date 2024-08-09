from django.urls import path
from config import views
from config.views import SongTopListView, SongNewListView, VideoNewListView, VideoTopListView, RasmTopListView, RasmNewListView, SherTopListView, SherNewListView, SongCompListView


urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.PROFILE, name='profile'),
    path('update-profile', views.Update_Profile, name='update_profile'),
   
    
    path('registration/', views.registration, name='registration'),
    path('verify/', views.verify, name='verify'),
    path('login/', views.Login, name='login'),
    path('callback/', views.AuthCallbackView.as_view(), name='callback'),
    path('tabs/single/', views.tabs_single, name='tabs_single'),
    path("top/music/", SongTopListView.as_view(), name="top_music"),
    path("new/music/", SongNewListView.as_view(), name="new_music"),
    path('top/video/', VideoTopListView.as_view(), name='top_video'),
    path('new/video/', VideoNewListView.as_view(), name='new_video'),
    path('top/photo/', RasmTopListView.as_view(), name='top_photo'),
    path('new/photo/', RasmNewListView.as_view(), name='new_photo'),
    path('top/sher/', SherTopListView.as_view(), name='top_sher'),
    path('new/sher/', SherNewListView.as_view(), name='new_sher'),
    path('aloqa/', views.aloqa, name='aloqa'),
    path('profile_user/<int:pk>', views.profile_user, name='profile_user'),
    path('ajax_sher/', views.ajax_sher, name='ajax_sher'),
    path('ajax_video/', views.ajax_video, name='ajax_video'),
    path('ajax_rasm/', views.ajax_rasm, name='ajax_rasm'),
    path('ajax_song/', views.ajax_song, name='ajax_song'),


    path('comp/song', views.SongCompListView, name='comp_song'),
    path('verify/song', views.verifySong, name='verify_song'),
    path('timeout', views.TimeOut, name='timeout'),


    path('comp/video', views.VideoCompListView, name='comp_video'),
    path('verify/video', views.VerifyVideo, name='verify_video'),

    path('comp/sher', views.SherCompListView, name='comp_sher'),
    path('verify/sher', views.VerifySher, name='verify_sher'),

    path('comp/rassom', views.RassomCompListView, name='comp_rassom'),
    path('verify/rassom', views.VerifyRassom, name='verify_rassom'),
 
]