from  django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Sher, Talant, Rassom, Videos, Song, CustomUser
from django.contrib import messages
from .forms import SherForm, RassomForm, VideoForm, SongForm
from django.views.generic import ListView
from config.utils import send_sms
import re


@login_required(login_url='login')
def manager_home(request):
    if request.user.user_type == "MANAGER":
        return render(request, 'backend/Manager/index.html')
    return redirect("logout")
# ================================= SHER =========================================
@login_required(login_url='login')
def VIEW_SHER(request):
    if request.user.user_type == "MANAGER":
        shers = Sher.objects.filter(deleted=False)

        context = {
            'shers':shers
        }
        return render(request, 'backend/Manager/pages/sher/list_sher.html', context)
    return redirect("logout")

@login_required(login_url='login')
def SherDetailView(request, pk):
    if request.user.user_type == "MANAGER":
        object = Sher.objects.get(id=pk)
        context = {
            'object':object,
        }
        return render(request, 'backend/Manager/pages/sher/each_sher_view.html', context)
    return redirect('logout')

@login_required(login_url='login')
def Active_Sher(request, pk):
    if request.user.user_type == "MANAGER":
        sher = Sher.objects.get(id=pk)
        tel = sher.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {sher.title} nomli she'ringiz faollashtirildi"
        send_sms(xabar, tel)
        sher.situation="Active"
        sher.save()
        messages.success(request, "She'r activlashtirildi")
        return redirect('view_sher_manager')
    return redirect('logout')

@login_required(login_url='login')
def InActive_Sher(request, pk):
    if request.user.user_type == "MANAGER":
        sher = Sher.objects.get(id=pk)
        tel = sher.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {sher.title} nomli she'ringiz faol emas"
        send_sms(xabar, tel)
        sher.situation="Inactive"
        sher.save()
        messages.success(request, "She'r faol emas")
        return redirect('view_sher_manager')
    return redirect('logout')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================= SONG =========================================
@login_required(login_url='login')
def LIST_SONGS(request):
    if request.user.user_type == "MANAGER":
        songs = Song.objects.filter(deleted=False)

        context = {
            'songs':songs
        }
        return render(request, 'backend/Manager/pages/song/list_song.html', context)
    return redirect('logout')


@login_required(login_url='login')
def SongDetailView(request, pk):
    if request.user.user_type == "MANAGER":
        object = Song.objects.get(id=pk)
        context = {
            'object':object,
        }
        return render(request, 'backend/Manager/pages/song/each_song_view.html', context)
    return redirect('logout')


@login_required(login_url='login')
def Active_Song(request, pk):
    if request.user.user_type == "MANAGER":
        song = Song.objects.get(id=pk)
        tel = song.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {song.song_title} nomli musicangiz faollashtirildi"
        send_sms(xabar, tel)
        song.situation="Active"
        song.save()
        messages.success(request, "Song activlashtirildi")
        return redirect('list_song_manager')
    return redirect('logout')


@login_required(login_url='login')
def InActive_Song(request, pk):
    if request.user.user_type == "MANAGER":
        song = Song.objects.get(id=pk)
        tel = song.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {song.song_title} nomli musicangiz faol emas"
        send_sms(xabar, tel)
        song.situation="Inactive"
        song.save()
        messages.success(request, "Song faol emas")
        return redirect('list_song_manager')

    return redirect('logout')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================= VIDEO =========================================
@login_required(login_url='login')
def LIST_VIDEOS(request):
    if request.user.user_type == "MANAGER":
        videos = Videos.objects.filter(deleted=False)

        context = {
            'videos':videos
        }
        return render(request, 'backend/Manager/pages/video/list_video.html', context)
    
    return redirect('logout')

@login_required(login_url='login')
def VideoDetailView(request, pk):
    if request.user.user_type == "MANAGER":
        object = Videos.objects.get(id=pk)
        context = {
            'object':object,
        }
        return render(request, 'backend/Manager/pages/video/each_video_view.html', context)
    return redirect('logout')

@login_required(login_url='login')
def Active_Video(request, pk):
    if request.user.user_type == "MANAGER":
        video = Videos.objects.get(id=pk)
        tel = video.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {video.title} nomli videoingiz faollashtirildi"
        send_sms(xabar, tel)
        video.situation="Active"
        video.save()
        messages.success(request, "She'r activlashtirildi")
        return redirect('list_video_manager')
    return redirect('logout')

@login_required(login_url='login')
def InActive_Video(request, pk):
    if request.user.user_type == "MANAGER":
        video = Videos.objects.get(id=pk)
        tel = video.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {video.title} nomli videoingiz faol emas"
        send_sms(xabar, tel)
        video.situation="Inactive"
        video.save()
        messages.success(request, "She'r faol emas")
        return redirect('list_video_manager')
    return redirect('logout')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================= RASSOM =========================================
class RassomList(ListView):
    model = Rassom
    template_name = "backend/Manager/pages/rassom/rassom_list.html"
    context_object_name = "rassoms"

    def get_queryset(self):
        if self.request.user.user_type == "MANAGER":
            return Rassom.objects.filter(deleted=False)

        return redirect('logout')
    
@login_required(login_url='login')
def RassomDetailView(request, pk):
    if request.user.user_type == "MANAGER":
        object = Rassom.objects.get(id=pk)
        context = {
            'object':object,
        }
        return render(request, 'backend/Manager/pages/rassom/each_rassom_view.html', context)
    return redirect('logout')

@login_required(login_url='login')
def Active_Rassom(request, pk):
    if request.user.user_type == "MANAGER":
        rassom = Rassom.objects.get(id=pk)
        tel = rassom.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {rassom.title} nomli rasmingiz faollashtirildi"
        send_sms(xabar, tel)
        rassom.situation="Active"
        rassom.save()
        messages.success(request, "She'r activlashtirildi")
        return redirect('list_rassoms_manager')
    return redirect('logout')

@login_required(login_url='login')
def InActive_Rassom(request, pk):
    if request.user.user_type == "MANAGER":
        rassom = Rassom.objects.get(id=pk)
        tel = rassom.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {rassom.title} nomli rasmingiz faol emas"
        send_sms(xabar, tel)
        rassom.situation="Inactive"
        rassom.save()
        messages.success(request, "She'r faol emas")
        return redirect('list_rassoms_manager')
    return redirect('logout')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


class TalantListView(ListView):
    model = Talant
    template_name = "backend/Manager/pages/artist/view_talant.html"
    # paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['talants'] = Talant.objects.all()
        return context

@login_required(login_url='login')
def TalantDetailView(request, pk):

    object = Talant.objects.get(id=pk)
    category_all = ""
    for i in object.taland_category.values():
        category_all = category_all + str(i['name'])+"|"
    context = {
        'object':object,
        'category_all':category_all,
    }
    return render(request, 'backend/Manager/pages/artist/each_view.html', context)

@login_required(login_url='login')
def DeleteTalant(request, pk):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    user = CustomUser.objects.get(id=pk)
    user.delete()
    messages.success(request, "Foydalanuvchi muvaffaqiyatli o'chirildi")
    return redirect('artist_lists')

@login_required(login_url='login')
def Active_User(request, pk):
    talant = CustomUser.objects.get(id=pk)
    talant_user = Talant.objects.get(artist=pk)
    talant.is_active=True
    talant.save()
    tel = talant_user.phone_number[1:]
    tel = re.sub('[^0-9]','', tel)
    send_sms("sizning accountingiz activlashtirildi", tel)
    messages.success(request, 'foydalanuvchi muvaffaqiyatli active boldi')
    return redirect('artist_lists')

@login_required(login_url='login')
def Inactive_User(request, pk):
    talant = CustomUser.objects.get(id=pk)
    talant_user = Talant.objects.get(artist=pk)
    talant.is_active=False
    talant.save()
    tel = talant_user.phone_number[1:]
    tel = re.sub('[^0-9]','', tel)
    send_sms("Sizning accountingiz vatincha ishchi holatida emas", tel)
    messages.success(request, 'foydalanuvchi muvaffaqiyatli inactive')
    return redirect('artist_lists')