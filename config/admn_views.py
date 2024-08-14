from  django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from config.models import *
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from config.utils import send_sms
import re




@login_required(login_url='login')
def admn_home(request):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    return render(request, 'backend/Admn/index.html')



# ========================================== TALANT ===============================================
@login_required(login_url='login')
def ADD_TALANT(request):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    categories = TalandCategory.objects.all()
    if request.method == 'POST':
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')
        login = request.POST.get('login')
        parol = request.POST.get('parol')
        rasm = request.FILES.get('rasm')
        category = request.POST.getlist('category')
        tel_number = request.POST.get('tel_number')
        
        if Talant.objects.filter(phone_number=tel_number).exists():
            messages.warning(request, 'Bunaqa telefon nomer bor')
            return redirect('add_talant')
        if CustomUser.objects.filter(username=login).exists():
            messages.warning(request, 'Bu nomli foydalanuvchi bor')
            return redirect('add_talant')

        
        user = CustomUser(first_name=ism, last_name=familya, username=login, profil_pic=rasm, user_type="USER")
        user.set_password(parol)
        user.save()
        artist_model = Talant(artist=user, phone_number=tel_number)
        artist_model.save()
        for i in category:
           artist_model.taland_category.add(TalandCategory.objects.get(id=i))
        messages.success(request, "Yangi foydalanuvchi qo/'shildi")
        return redirect('view_talant')

    context = {
        'categories':categories,
    }
    return render(request, 'backend/Admn/pages/users/add_talant.html', context)


class ArtistListView(ListView):
    model = Talant
    template_name = "backend/Admn/pages/users/view_talant.html"
    # paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['talants'] = Talant.objects.all()
        return context


@login_required(login_url='login')
def ArtistDetailView(request, pk):

    object = Talant.objects.get(id=pk)
    category_all = ""
    for i in object.taland_category.values():
        category_all = category_all + str(i['name'])+"|"
    context = {
        'object':object,
        'category_all':category_all,
    }
    return render(request, 'backend/Admn/pages/users/each_view.html', context)



@login_required(login_url='login')
def EditTalant(request, pk):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    talant = Talant.objects.get(id=pk)
    

    category_selected = talant.taland_category.values()
    categories = TalandCategory.objects.all()
    
    for i in category_selected:
        categories = categories.exclude(id=i['id'])
    context = {
        'talant':talant,
        'categories':categories,
        'category_selected':category_selected,
    }
    return render(request, 'backend/Admn/pages/users/update_user.html', context)

@login_required(login_url='login')
def UpdateTalant(request):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    
    if request.method == "POST":
        artist_id = request.POST.get('artist_id')
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')
        category = request.POST.getlist('category')
        tel_raqam = request.POST.get('tel_number')
        login = request.POST.get('login')
        parol = request.POST.get('parol')
        rasm = request.FILES.get('rasm')
        user = CustomUser.objects.get(id=artist_id)
        user.first_name = ism
        user.last_name = familya

        if parol != None and parol != "":
            user.set_password(parol)
        if rasm != None and rasm != "":
            user.profil_pic = rasm
        user.save()

        artist = Talant.objects.get(artist=artist_id)
        # category_model = TalandCategory.objects.get(id=category_id)
        artist.taland_category.set('')

        artist.save()
        for i in category:
           artist.taland_category.add(TalandCategory.objects.get(id=i))
        messages.success(request, "Foydalanuchining malumotlari muvaffaqiyotli yangilandi")
        return redirect('view_talant')


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
    return redirect('view_talant')

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
    return redirect('view_talant')

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
    return redirect('view_talant')
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# =========================================== MANAGER ================================================
@login_required(login_url='login')
def ADD_MANAGER(request):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    if request.method == 'POST':
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')
        login = request.POST.get('login')
        parol = request.POST.get('parol')
        rasm = request.FILES.get('rasm')
        
        if CustomUser.objects.filter(username=login).exists():
            messages.warning(request, 'Bu nomli foydalanuvchi bor')
            return redirect('add_manager')

        
        user = CustomUser(first_name=ism, last_name=familya, username=login, user_type="MANAGER", profil_pic=rasm)
        user.set_password(parol)
        user.save()
        manager_model = Managers(manager=user)
        manager_model.save()
        messages.success(request, "Yangi foydalanuvchi qo/'shildi")
        return redirect('view_manager')

    context = {
    }
    return render(request, 'backend/Admn/pages/manager/add_manager.html', context)


class ManagerListView(ListView):
    model = Managers
    template_name = "backend/Admn/pages/manager/view_manager.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['managers'] = Managers.objects.all()
        return context
        
    

class ManagerDetailView(DetailView):
    model = Managers
    template_name = "backend/Admn/pages/manager/each_manager_view.html"

@login_required(login_url='login')
def ManagerEdit(request, pk):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    manager = Managers.objects.get(id=pk)
    context = {
        'manager':manager,
    }
    return render(request, 'backend/Admn/pages/manager/update_manager.html', context)


@login_required(login_url='login')
def UpdateManager(request):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    if request.method == "POST":
        manager_id = request.POST.get('manager_id')
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')
        login = request.POST.get('login')
        parol = request.POST.get('parol')
        rasm = request.FILES.get('rasm')

        user = CustomUser.objects.get(id=manager_id)
        user.first_name = ism
        user.last_name = familya
        if parol != None and parol != "":
            user.set_password(parol)
        if rasm != None and rasm != "":
            user.profil_pic = rasm
        user.save()

        messages.success(request, 'Foydalanuchining malumotlari muvaffaqiyotli yangilandi')
        return redirect('view_manager')
    
@login_required(login_url='login')
def DeleteManager(request, pk):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    user = CustomUser.objects.get(id=pk)
    user.delete()
    messages.success(request, "Foydalanuvchi muvaffaqiyatli o'chirildi")
    return redirect('view_manager')

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-


# ====================================== CATEGORY ===============================================
@login_required(login_url='login')
def CATEGORY(request):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    categories = TalandCategory.objects.all()
    if request.method == 'POST':
        category_nomi = request.POST.get('category_nomi')
        if TalandCategory.objects.filter(name=category_nomi).exists():
            messages.warning(request, 'Bunaqa nom bilan allaqachon categoriya kiritilgan')
            return redirect('category')
        category_model = TalandCategory(name=category_nomi, whofrom=request.user)
        category_model.save()
        messages.success(request, "Categoriya muvaffaqiyatli qo'shildi")
        return redirect('category')

    context = {
        'categories':categories,
    } 
    return render(request, 'backend/Admn/pages/category/category.html', context)

@login_required(login_url='login')
def DeleteCategory(request, pk):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    category_model = TalandCategory.objects.get(id=pk)
    category_model.delete()
    messages.success(request, "Category muvaffaqiyatli o'chiqirildi")
    return redirect('category')

@login_required(login_url='login')
def Update_category(request):
    if request.user.user_type !='ADMIN':
        if request.user.user_type == 'MANAGER':
            return redirect('manager_home')
        else:
            return redirect('talant_home')
    if request.method == 'POST':
        category_updated_name = request.POST.get('category_updated_name')
        category_updated_id = request.POST.get('category_updated_id')
        if TalandCategory.objects.filter(name=category_updated_name).exists():
            messages.warning(request, 'Bu turdagi category nomi kiritilgan')
            return redirect('category')
        category_updated_model = TalandCategory.objects.get(id=category_updated_id)
        category_updated_model.name=category_updated_name
        category_updated_model.save()
        messages.success(request, 'Categoriya muvaffaqiyatli yangilandi')
        return redirect('category')
    
# ================================= SHER =========================================
@login_required(login_url='login')
def VIEW_SHER(request):
    if request.user.user_type == "ADMIN":
        shers = Sher.objects.filter(deleted=False)

        context = {
            'shers':shers
        }
        return render(request, 'backend/Admn/pages/sher/list_sher.html', context)
    return redirect("logout")

@login_required(login_url='login')
def SherDetailView(request, pk):
    if request.user.user_type == "ADMIN":
        object = Sher.objects.get(id=pk)
        context = {
            'object':object,
        }
        return render(request, 'backend/Admn/pages/sher/each_sher_view.html', context)
    return redirect('logout')

@login_required(login_url='login')
def Active_Sher(request, pk):
    if request.user.user_type == "ADMIN":
        sher = Sher.objects.get(id=pk)
        tel = sher.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {sher.title} nomli she'ringiz faollashtirildi"
        send_sms(xabar, tel)
        sher.situation="Active"
        sher.save()
        messages.success(request, "She'r activlashtirildi")
        return redirect('sher_list_A')
    return redirect('logout')

@login_required(login_url='login')
def InActive_Sher(request, pk):
    if request.user.user_type == "ADMIN":
        sher = Sher.objects.get(id=pk)
        tel = sher.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {sher.title} nomli she'ringiz faol emas"
        send_sms(xabar, tel)
        sher.situation="Inactive"
        sher.save()
        messages.success(request, "She'r faol emas")
        return redirect('sher_list_A')
    return redirect('logout')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================= SONG =========================================
@login_required(login_url='login')
def LIST_SONGS(request):
    if request.user.user_type == "ADMIN":
        songs = Song.objects.filter(deleted=False)

        context = {
            'songs':songs
        }
        return render(request, 'backend/Admn/pages/song/list_song.html', context)
    return redirect('logout')


@login_required(login_url='login')
def SongDetailView(request, pk):
    if request.user.user_type == "ADMIN":
        object = Song.objects.get(id=pk)
        context = {
            'object':object,
        }
        return render(request, 'backend/Admn/pages/song/each_song_view.html', context)
    return redirect('logout')


@login_required(login_url='login')
def Active_Song(request, pk):
    if request.user.user_type == "ADMIN":
        song = Song.objects.get(id=pk)
        tel = song.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {song.song_title} nomli musicangiz faollashtirildi"
        send_sms(xabar, tel)
        song.situation="Active"
        song.save()
        messages.success(request, "Song activlashtirildi")
        return redirect('list_song_A')
    return redirect('logout')


@login_required(login_url='login')
def InActive_Song(request, pk):
    if request.user.user_type == "ADMIN":
        song = Song.objects.get(id=pk)
        tel = song.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {song.song_title} nomli musicangiz faol emas"
        send_sms(xabar, tel)
        song.situation="Inactive"
        song.save()
        messages.success(request, "Song faol emas")
        return redirect('list_song_A')

    return redirect('logout')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


# ================================= VIDEO =========================================
@login_required(login_url='login')
def LIST_VIDEOS(request):
    if request.user.user_type == "ADMIN":
        videos = Videos.objects.filter(deleted=False)

        context = {
            'videos':videos
        }
        return render(request, 'backend/Admn/pages/video/list_video.html', context)
    
    return redirect('logout')

@login_required(login_url='login')
def VideoDetailView(request, pk):
    if request.user.user_type == "ADMIN":
        object = Videos.objects.get(id=pk)
        context = {
            'object':object,
        }
        return render(request, 'backend/Admn/pages/video/each_video_view.html', context)
    return redirect('logout')

@login_required(login_url='login')
def Active_Video(request, pk):
    if request.user.user_type == "ADMIN":
        video = Videos.objects.get(id=pk)
        tel = video.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {video.title} nomli videoingiz faollashtirildi"
        send_sms(xabar, tel)
        video.situation="Active"
        video.save()
        messages.success(request, "She'r activlashtirildi")
        return redirect('list_video_A')
    return redirect('logout')

@login_required(login_url='login')
def InActive_Video(request, pk):
    if request.user.user_type == "ADMIN":
        video = Videos.objects.get(id=pk)
        tel = video.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {video.title} nomli videoingiz faol emas"
        send_sms(xabar, tel)
        video.situation="Inactive"
        video.save()
        messages.success(request, "She'r faol emas")
        return redirect('list_video_A')
    return redirect('logout')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


# ================================= RASSOM =========================================
class RassomList(ListView):
    model = Rassom
    template_name = "backend/Admn/pages/rassom/rassom_list.html"
    context_object_name = "rassoms"

    def get_queryset(self):
        if self.request.user.user_type == "ADMIN":
            return Rassom.objects.filter(deleted=False)

        return redirect('logout')
    
@login_required(login_url='login')
def RassomDetailView(request, pk):
    if request.user.user_type == "ADMIN":
        object = Rassom.objects.get(id=pk)
        context = {
            'object':object,
        }
        return render(request, 'backend/Admn/pages/rassom/each_rassom_view.html', context)
    return redirect('logout')

@login_required(login_url='login')
def Active_Rassom(request, pk):
    if request.user.user_type == "ADMIN":
        rassom = Rassom.objects.get(id=pk)
        tel = rassom.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {rassom.title} nomli rasmingiz faollashtirildi"
        send_sms(xabar, tel)
        rassom.situation="Active"
        rassom.save()
        messages.success(request, "She'r activlashtirildi")
        return redirect('list_rassoms_A')
    return redirect('logout')

@login_required(login_url='login')
def InActive_Rassom(request, pk):
    if request.user.user_type == "ADMIN":
        rassom = Rassom.objects.get(id=pk)
        tel = rassom.user.phone_number[1:]
        tel = re.sub('[^0-9]','', tel)
        xabar = f"Siz kiritgan {rassom.title} nomli rasmingiz faol emas"
        send_sms(xabar, tel)
        rassom.situation="Inactive"
        rassom.save()
        messages.success(request, "She'r faol emas")
        return redirect('list_rassoms_A')
    return redirect('logout')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


# ============================= ARCHIVES ===========================================
@login_required(login_url='login')
def Archive_Sher(request):
    if request.user.user_type == "ADMIN":
        shers = Sher.objects.filter(deleted=True)

        context = {
            'shers':shers
        }
        return render(request, 'backend/Admn/pages/Archives/sher.html', context)
    return redirect("logout")

@login_required(login_url='login')
def Archive_Rassom(request):
    if request.user.user_type == "ADMIN":
        rassoms = Rassom.objects.filter(deleted=True)

        context = {
            'rassoms':rassoms
        }
        return render(request, 'backend/Admn/pages/Archives/rassom.html', context)
    return redirect("logout")

@login_required(login_url='login')
def Archive_Song(request):
    if request.user.user_type == "ADMIN":
        songs = Song.objects.filter(deleted=True)

        context = {
            'songs':songs
        }
        return render(request, 'backend/Admn/pages/Archives/song.html', context)
    return redirect("logout")

@login_required(login_url='login')
def Archive_Video(request):
    if request.user.user_type == "ADMIN":
        videos = Videos.objects.filter(deleted=True)

        context = {
            'videos':videos
        }
        return render(request, 'backend/Admn/pages/Archives/video.html', context)
    return redirect("logout")
