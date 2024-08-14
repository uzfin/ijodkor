import os
import pytz
from datetime import datetime, timedelta
import datetime
import re
import requests
import random
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout
from config.LoginBackend import LoginBackend
from config.models import TalandCategory, Sher, Song, Videos,Counter, Comp_Song, Phone_numbers, SmsPhoneVerify, Comp_Video, Comp_Rassom
from config.utils import send_sms, generateCode, oAuth2Client
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View


def get_object_or_none(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        obj = None
    return obj

def index(request):
    sherlar = Sher.objects.filter(situation="Active", deleted=False).order_by("-id")[:6]
    qiymat = request.GET.get('button_text')
    songs_top = Song.objects.filter(situation='Active', deleted=False).order_by("-like")[:6]
    songs_new = Song.objects.filter(situation='Active', deleted=False).order_by("-id")[:6]
    videos = Videos.objects.filter(situation='Active', deleted=False).order_by("-id")[:6]
    rasmlar = Rassom.objects.filter(situation="Active", deleted=False).order_by("-id")[:6]
    try:
        counter = Counter.objects.get(id=1)
    except Counter.DoesNotExist:
        counter = {}

    oauth2client = oAuth2Client(
        client_id="6",
        client_secret="Lmf34scxVvECzfF4ljXAe7sIdVjJ1hO6nq6-7c7E",
        redirect_uri="https://24eb-195-158-14-110.ngrok-free.app/callback/",
        authorize_url="https://student.uzfi.uz/oauth/authorize",
        token_url="https://student.uzfi.uz/oauth/access-token",
        resource_owner_url="https://student.uzfi.uz/oauth/api/user?fields=id,uuid,type,name,login,picture,email,university_id,phone"
    )

    if qiymat != None:
        request.session['cached_session_key'] = request.session.session_key
        if request.session.get('cached_session_key') != None:
            if LikeID.objects.filter(like_name=request.session.get('cached_session_key')).exists():
                pass
            else:
                likemodel = LikeID(like_name=request.session.get('cached_session_key'))
                likemodel.save()
            
            sher = Sher.objects.get(id=int(qiymat))
            for i in sher.like.values():
                if i['like_name'] == request.session.get('cached_session_key'):
                    related_object = get_object_or_404(LikeID, like_name=request.session.get('cached_session_key'))
                    sher.like.remove(related_object)
                    sher.save()
                    return JsonResponse({'qiymat':sher.like.count()}, status=200)
                   
            sher.like.add(LikeID.objects.get(like_name=request.session.get('cached_session_key')))
            sher.save()
            return JsonResponse({'qiymat':sher.like.count()}, status=200)

    context = {
       'sherlar':sherlar,
       'songs_top':songs_top,
       'songs_new':songs_new,
       'videos':videos,
       'rasmlar':rasmlar,
        'counter':counter,
        "hemis_auth_url": oauth2client.get_authorization_url(),
    }
    return render(request,'frontend/main/index.html', context)



def registration(request):
   categories = TalandCategory.objects.all()
   if request.method == 'POST':
        request.session['ism'] = request.POST.get('ism')
        request.session['familya'] = request.POST.get('familya')
        request.session['tel'] = request.POST.get('tel')
        request.session['category'] = request.POST.getlist('category')
        request.session['login'] = request.POST.get('login')
        request.session['password'] = request.POST.get('password')


        session_key = request.FILES['file']

        file_path = os.path.join(settings.SESSION_FILE_PATH, str(session_key))
        print(file_path)

        tel = request.POST.get('tel')[1:]
        tel = re.sub('[^0-9]','', tel)

        if Artists.objects.filter(phone_number=request.session.get('tel')).exists():
            messages.warning(request, 'Bunaqa telefon nomer bor')
            return redirect('registration')
        if CustomUser.objects.filter(username=request.session.get('login')).exists():
            messages.warning(request, 'Bunaqa nomli foydalanuvchi bor')
            return redirect('registration')

        number_list = [x for x in range(10)]
        code_items = []

        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)
        code_string = "".join(str(item) for item in code_items)
        request.session['code_string'] = code_string
        send_sms(code_string, tel)

        return redirect('verify')

   context = {
      'categories':categories,
   }
   return render(request, 'login/registration.html', context)

def verify(request):
   if request.method == 'POST':
    code = request.POST.get('code')
    
    if code != None and request.session.get('code_string') != None:
        if code == request.session.get('code_string'):
            user = CustomUser(first_name=request.session.get('ism'), last_name=request.session.get('familya'), username=request.session.get('login'), profil_pic=request.session.get('rasm'), user_type="USER")
            user.set_password(request.session.get('password'))
            user.is_active=False
            user.save()
            artist_model = Artists(artist=user, phone_number=request.session.get('tel'))
            artist_model.save()
            for i in request.session.get('category'):
                artist_model.taland_category.add(TalandCategory.objects.get(id=i))
            messages.success(request, "Yangi foydalanuvchi qo/'shildi")
            request.session.clear()
            return redirect('talant_home')
        else:
            messages.error(request, 'Tasdiqlash kodi notogri')
            return redirect('verify')
    else:
        print('remove all of thing')
      
   return render(request, 'login/verify.html')

def Login(request):
    
    return render(request, 'login/login.html')

def doLogin(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=LoginBackend.authenticate(request, username=request.POST.get('login'), password=request.POST.get('password'))
        if user!=None and user.is_active == True:
            login(request, user)
            if user.user_type=="ADMIN":
                return HttpResponseRedirect('Admn/home')
            elif user.user_type=="MANAGER":
                return HttpResponseRedirect('Manager/home')
            elif user.user_type=="USER":
                return HttpResponseRedirect('Talant/home')
        else:
            messages.error(request, 'Login yoki parol xato')
            return HttpResponseRedirect('login/')

def Logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='login')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        'user':user,
    }
    return render(request, 'backend/main/profile.html', context)

def Update_Profile(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        ism = request.POST.get('ism')
        familya = request.POST.get('familya')
        rasm  = request.FILES.get('rasm')
        user_model = CustomUser.objects.get(id=user_id)
        user_model.first_name = ism
        user_model.last_name = familya
      
        if rasm != None and rasm != "":
            user_model.profil_pic = rasm
        user_model.save()
        messages.success(request, 'Bu foydalanuvchi malumotlari muvaffaqiyatli yangilandi')
        if user_model.user_type == "ADMIN":
           return redirect('admn_home')
        elif user_model.user_type == 'MANAGER':
           return redirect('manager_home')
        else:
           return redirect('talant_home')

    
    return render(request, 'backend/main/profile.html')

      


def tabs_single(request):
 return render(request,'tabs-single.html')


class SongTopListView(ListView):
    model = Song
    template_name = "frontend/pages/top_music.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(SongTopListView, self).get_context_data(**kwargs) 
        list_exam = Song.objects.filter(situation='Active', deleted=False).order_by("-like")
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_exams'] = file_exams
        return context

class SongNewListView(ListView):
    model = Song
    template_name = "frontend/pages/new_music.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(SongNewListView, self).get_context_data(**kwargs) 
        list_exam = Song.objects.filter(situation='Active', deleted=False).order_by("-id")
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_exams'] = file_exams
        return context


class VideoTopListView(ListView):
    model = Videos
    template_name = "frontend/pages/top_video.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(VideoTopListView, self).get_context_data(**kwargs) 
        list_exam = Videos.objects.filter(situation='Active', deleted=False).order_by("-like")
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_exams'] = file_exams
        return context

class VideoNewListView(ListView):
    model = Videos
    template_name = "frontend/pages/new_video.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(VideoNewListView, self).get_context_data(**kwargs) 
        list_exam = Videos.objects.filter(situation='Active', deleted=False).order_by("-id")
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_exams'] = file_exams
        return context

class RasmTopListView(ListView):
    model = Rassom
    template_name = "frontend/pages/top_photo.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(RasmTopListView, self).get_context_data(**kwargs) 
        list_exam = Rassom.objects.filter(situation='Active', deleted=False).order_by("-like")
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_exams'] = file_exams
        return context

class RasmNewListView(ListView):
    model = Rassom
    template_name = "frontend/pages/new_photo.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(RasmNewListView, self).get_context_data(**kwargs) 
        list_exam = Rassom.objects.filter(situation='Active', deleted=False).order_by("-id")
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_exams'] = file_exams
        return context

class SherTopListView(ListView):
    model = Sher
    template_name = "frontend/pages/top_sher.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(SherTopListView, self).get_context_data(**kwargs) 
        list_exam = Sher.objects.filter(situation='Active', deleted=False).order_by("-like")
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_exams'] = file_exams
        return context

class SherNewListView(ListView):
    model = Sher
    template_name = "frontend/pages/new_sher.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(SherNewListView, self).get_context_data(**kwargs) 
        list_exam = Sher.objects.filter(situation='Active', deleted=False).order_by("-id")
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_exams'] = file_exams
        return context
    
def ajax_sher(request):
    qiymat = request.GET.get('button_text')
    if qiymat != None:
        request.session['cached_session_key'] = request.session.session_key
        if request.session.get('cached_session_key') != None:
            if LikeID.objects.filter(like_name=request.session.get('cached_session_key')).exists():
                pass
            else:
                likemodel = LikeID(like_name=request.session.get('cached_session_key'))
                likemodel.save()
            
            sher = Sher.objects.get(id=int(qiymat))
            for i in sher.like.values():
                if i['like_name'] == request.session.get('cached_session_key'):
                    related_object = get_object_or_404(LikeID, like_name=request.session.get('cached_session_key'))
                    sher.like.remove(related_object)
                    sher.save()
                    return JsonResponse({'qiymat':sher.like.count()}, status=200, safe=False)
                
        sher.like.add(LikeID.objects.get(like_name=request.session.get('cached_session_key')))
        sher.save()
        return JsonResponse({'qiymat':sher.like.count()}, status=200, safe=False)
    
def ajax_video(request):
    qiymat = request.GET.get('button_text')
    if qiymat != None:
        request.session['cached_session_key'] = request.session.session_key
        if request.session.get('cached_session_key') != None:
            if LikeID.objects.filter(like_name=request.session.get('cached_session_key')).exists():
                pass
            else:
                likemodel = LikeID(like_name=request.session.get('cached_session_key'))
                likemodel.save()
            
            video = Videos.objects.get(id=int(qiymat))
            for i in video.like.values():
                if i['like_name'] == request.session.get('cached_session_key'):
                    related_object = get_object_or_404(LikeID, like_name=request.session.get('cached_session_key'))
                    video.like.remove(related_object)
                    video.save()
                    return JsonResponse({'qiymat':video.like.count()}, status=200, safe=False)
                
        video.like.add(LikeID.objects.get(like_name=request.session.get('cached_session_key')))
        video.save()
        return JsonResponse({'qiymat':video.like.count()}, status=200, safe=False)

def ajax_rasm(request):
    qiymat = request.GET.get('button_text')
    if qiymat != None:
        request.session['cached_session_key'] = request.session.session_key
        if request.session.get('cached_session_key') != None:
            if LikeID.objects.filter(like_name=request.session.get('cached_session_key')).exists():
                pass
            else:
                likemodel = LikeID(like_name=request.session.get('cached_session_key'))
                likemodel.save()
            
            rasm = Rassom.objects.get(id=int(qiymat))
            for i in rasm.like.values():
                if i['like_name'] == request.session.get('cached_session_key'):
                    related_object = get_object_or_404(LikeID, like_name=request.session.get('cached_session_key'))
                    rasm.like.remove(related_object)
                    rasm.save()
                    return JsonResponse({'qiymat':rasm.like.count()}, status=200, safe=False)
                
        rasm.like.add(LikeID.objects.get(like_name=request.session.get('cached_session_key')))
        rasm.save()
        return JsonResponse({'qiymat':rasm.like.count()}, status=200, safe=False)
    

def ajax_song(request):
    qiymat = request.GET.get('button_text')
    if qiymat != None:
        request.session['cached_session_key'] = request.session.session_key
        if request.session.get('cached_session_key') != None:
            if LikeID.objects.filter(like_name=request.session.get('cached_session_key')).exists():
                pass
            else:
                likemodel = LikeID(like_name=request.session.get('cached_session_key'))
                likemodel.save()
            
            song = Song.objects.get(id=int(qiymat))
            for i in song.like.values():
                if i['like_name'] == request.session.get('cached_session_key'):
                    related_object = get_object_or_404(LikeID, like_name=request.session.get('cached_session_key'))
                    song.like.remove(related_object)
                    song.save()
                    return JsonResponse({'qiymat':song.like.count()}, status=200, safe=False)
                
        song.like.add(LikeID.objects.get(like_name=request.session.get('cached_session_key')))
        song.save()
        return JsonResponse({'qiymat':song.like.count()}, status=200, safe=False)

def aloqa(request):
    return render(request,'frontend/pages/aloqa.html')

def profile_user(request, pk):
    user_picture = CustomUser.objects.get(id=pk)
    artist_user = Artists.objects.get(artist=user_picture)
    rasm_user = Rassom.objects.filter(user=artist_user, situation='Active', deleted=False)
    song_user = Song.objects.filter(user=artist_user, situation='Active', deleted=False)
    video_user = Videos.objects.filter(user=artist_user, situation='Active', deleted=False)
    sher_user = Sher.objects.filter(user=artist_user, situation='Active', deleted=False)
    
    context = {
        'user_picture':user_picture,
        'artist_user':artist_user,
        'rasm_user':rasm_user,
        'song_user':song_user,
        'video_user':video_user,
        'sher_user':sher_user,
    }
    return render(request,'frontend/pages/prof.html', context)

def SongCompListView(request):
    counter_model = Counter.objects.get(id=1)
    datetime_object = datetime.datetime(counter_model.year, counter_model.month, counter_model.day)
    utc=pytz.UTC
    current_datetime = timezone.now() + timedelta(hours=5)
    expired_on = datetime_object.replace(tzinfo=utc)
    checked_on = current_datetime.replace(tzinfo=utc)
    if expired_on > checked_on and counter_model.competition == "Music":
        song_comp = Comp_Song.objects.all()
        if request.method == 'POST':
            phone_number = request.POST.get('phone_number')
            product_id = request.POST.get('product_id')
            
            phone_number = request.POST.get('phone_number')[1:]
            phone_number = re.sub('[^0-9]','', phone_number)

            code = generateCode()
            if Phone_numbers.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'Bu raqam allaqachon tasdiqlangan')
                return redirect('comp_song')
            verification_code = SmsPhoneVerify.objects.get_or_create(code=code, phone_number=phone_number, product_id=product_id)[0]

            try:
                send_sms(code, phone_number)
            except Exception as error:
                messages.error(request, str(error))
                return redirect('comp_song')
            
            return redirect('verify_song')
        context = {
            'song_comp':song_comp,
        }
        return render(request,'frontend/competition/song/comp_song.html', context)
    else:
        return redirect('timeout')

def verifySong(request):
    counter_model = Counter.objects.get(id=1)
    datetime_object = datetime.datetime(counter_model.year, counter_model.month, counter_model.day)
    utc=pytz.UTC
    current_datetime = timezone.now() + timedelta(hours=5)
    expired_on = datetime_object.replace(tzinfo=utc)
    checked_on = current_datetime.replace(tzinfo=utc)
    if expired_on > checked_on and counter_model.competition == "Music":
        song_comp = Comp_Song.objects.all()

        if request.method == 'POST':
            verify_code = request.POST.get('verify_code')

            try:
                verify_code_model = SmsPhoneVerify.objects.get(code = verify_code)
                utc=pytz.UTC
                current_datetime = timezone.now() + timedelta(hours=5)
                time = verify_code_model.publishing_date + timedelta(hours=5, minutes=1)
                expired_on = time.replace(tzinfo=utc)
                checked_on = current_datetime.replace(tzinfo=utc)
                if expired_on > checked_on:
                    Phone_numbers.objects.create(phone_number=verify_code_model.phone_number)
                    comp_product_detail = Comp_Song.objects.get(id=verify_code_model.product_id)
                    comp_product_detail.votes.add(Phone_numbers.objects.get(phone_number=verify_code_model.phone_number))
                    comp_product_detail.save()
                    
                    messages.success(request, 'Tasdiqlash muvaffaqiyatli amalga oshirildi')
                    return redirect('comp_song')
                else:
                    messages.error(request, 'Tasdiqlash kodi xato')
                    return redirect('verify_song')
            except:
                messages.error(request, 'Kutilmagan xato')
                return redirect('verify_song')
            finally:
                verify_code_model = get_object_or_none(SmsPhoneVerify, code = verify_code)
                if verify_code_model is None:
                    pass
                else:
                    verify_code_model.delete()
        context = {
            'song_comp':song_comp,
        }
        return render(request,'frontend/competition/song/verify_song.html', context)
    else:
        return redirect('timeout')
    


def VideoCompListView(request):
    counter_model = Counter.objects.get(id=1)
    datetime_object = datetime.datetime(counter_model.year, counter_model.month, counter_model.day)
    utc=pytz.UTC
    current_datetime = timezone.now() + timedelta(hours=5)
    expired_on = datetime_object.replace(tzinfo=utc)
    checked_on = current_datetime.replace(tzinfo=utc)
    if expired_on > checked_on and counter_model.competition == "Video":
        video_comp = Comp_Video.objects.all()
        if request.method == 'POST':
            phone_number = request.POST.get('phone_number')
            product_id = request.POST.get('product_id')
            
            phone_number = request.POST.get('phone_number')[1:]
            phone_number = re.sub('[^0-9]','', phone_number)

            code = generateCode()
            if Phone_numbers.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'Bu raqam allaqachon tasdiqlangan')
                return redirect('comp_video')
            verification_code = SmsPhoneVerify.objects.get_or_create(code=code, phone_number=phone_number, product_id=product_id)[0]

            try:
                send_sms(code, phone_number)
            except Exception as error:
                messages.error(request, str(error))
                return redirect('verify_video')
            
            return redirect('verify_video')
        context = {
            'video_comp':video_comp,
        }
        return render(request,'frontend/competition/video/comp_video.html', context)
    else:
        return redirect('timeout')



def VerifyVideo(request):
    counter_model = Counter.objects.get(id=1)
    datetime_object = datetime.datetime(counter_model.year, counter_model.month, counter_model.day)
    utc=pytz.UTC
    current_datetime = timezone.now() + timedelta(hours=5)
    expired_on = datetime_object.replace(tzinfo=utc)
    checked_on = current_datetime.replace(tzinfo=utc)
    if expired_on > checked_on and counter_model.competition == "Video":
        video_comp = Comp_Video.objects.all()

        if request.method == 'POST':
            verify_code = request.POST.get('verify_code')

            try:
                verify_code_model = SmsPhoneVerify.objects.get(code = verify_code)
                utc=pytz.UTC
                current_datetime = timezone.now() + timedelta(hours=5)
                time = verify_code_model.publishing_date + timedelta(hours=5, minutes=1)
                expired_on = time.replace(tzinfo=utc)
                checked_on = current_datetime.replace(tzinfo=utc)
                if expired_on > checked_on:
                    Phone_numbers.objects.create(phone_number=verify_code_model.phone_number)
                    comp_product_detail = Comp_Video.objects.get(id=verify_code_model.product_id)
                    comp_product_detail.votes.add(Phone_numbers.objects.get(phone_number=verify_code_model.phone_number))
                    comp_product_detail.save()
                    
                    messages.success(request, 'Tasdiqlash muvaffaqiyatli amalga oshirildi')
                    return redirect('comp_video')
                else:
                    messages.error(request, 'Tasdiqlash kodi xato')
                    return redirect('verify_video')
            except SmsPhoneVerify.DoesNotExist:
                messages.error(request, 'Kutilmagan xato')
                return redirect('verify_video')
            finally:
                verify_code_model = get_object_or_none(SmsPhoneVerify, code = verify_code)
                if verify_code_model is None:
                    pass
                else:
                    verify_code_model.delete()
        context = {
            'video_comp':video_comp,
        }
        return render(request,'frontend/competition/video/verify_video.html', context)
    else:
        return redirect('timeout')
    

def SherCompListView(request):
    counter_model = Counter.objects.get(id=1)
    datetime_object = datetime.datetime(counter_model.year, counter_model.month, counter_model.day)
    utc=pytz.UTC
    current_datetime = timezone.now() + timedelta(hours=5)
    expired_on = datetime_object.replace(tzinfo=utc)
    checked_on = current_datetime.replace(tzinfo=utc)
    if expired_on > checked_on and counter_model.competition == "Writer":
        sher_comp = Comp_Sher.objects.all()
        if request.method == 'POST':
            phone_number = request.POST.get('phone_number')
            product_id = request.POST.get('product_id')
            
            phone_number = request.POST.get('phone_number')[1:]
            phone_number = re.sub('[^0-9]','', phone_number)

            code = generateCode()
            if Phone_numbers.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'Bu raqam allaqachon tasdiqlangan')
                return redirect('comp_sher')
            verification_code = SmsPhoneVerify.objects.get_or_create(code=code, phone_number=phone_number, product_id=product_id)[0]

            try:
                send_sms(code, phone_number)
            except Exception as error:
                messages.error(request, str(error))
                return redirect('verify_sher')
            
            return redirect('verify_sher')
        context = {
            'sher_comp':sher_comp,
        }
        return render(request,'frontend/competition/sher/comp_sher.html', context)
    else:
        return redirect('timeout')
    
def VerifySher(request):
    counter_model = Counter.objects.get(id=1)
    datetime_object = datetime.datetime(counter_model.year, counter_model.month, counter_model.day)
    utc=pytz.UTC
    current_datetime = timezone.now() + timedelta(hours=5)
    expired_on = datetime_object.replace(tzinfo=utc)
    checked_on = current_datetime.replace(tzinfo=utc)
    if expired_on > checked_on and counter_model.competition == "Writer":
        sher_comp = Comp_Sher.objects.all()

        if request.method == 'POST':
            verify_code = request.POST.get('verify_code')

            try:
                verify_code_model = SmsPhoneVerify.objects.get(code = verify_code)
                utc=pytz.UTC
                current_datetime = timezone.now() + timedelta(hours=5)
                time = verify_code_model.publishing_date + timedelta(hours=5, minutes=1)
                expired_on = time.replace(tzinfo=utc)
                checked_on = current_datetime.replace(tzinfo=utc)
                if expired_on > checked_on:
                    Phone_numbers.objects.create(phone_number=verify_code_model.phone_number)
                    comp_product_detail = Comp_Sher.objects.get(id=verify_code_model.product_id)
                    comp_product_detail.votes.add(Phone_numbers.objects.get(phone_number=verify_code_model.phone_number))
                    comp_product_detail.save()
                    
                    messages.success(request, 'Tasdiqlash muvaffaqiyatli amalga oshirildi')
                    return redirect('comp_sher')
                else:
                    messages.error(request, 'Tasdiqlash kodi xato')
                    return redirect('verify_sher')
            except SmsPhoneVerify.DoesNotExist:
                messages.error(request, 'Kutilmagan xato')
                return redirect('verify_sher')
            finally:
                verify_code_model = get_object_or_none(SmsPhoneVerify, code = verify_code)
                if verify_code_model is None:
                    pass
                else:
                    verify_code_model.delete()
        context = {
            'sher_comp':sher_comp,
        }
        return render(request,'frontend/competition/sher/verify_sher.html', context)
    else:
        return redirect('timeout')
    

def RassomCompListView(request):
    counter_model = Counter.objects.get(id=1)
    datetime_object = datetime.datetime(counter_model.year, counter_model.month, counter_model.day)
    utc=pytz.UTC
    current_datetime = timezone.now() + timedelta(hours=5)
    expired_on = datetime_object.replace(tzinfo=utc)
    checked_on = current_datetime.replace(tzinfo=utc)
    if expired_on > checked_on and counter_model.competition == "Painting":
        rassom_comp = Comp_Rassom.objects.all()
        if request.method == 'POST':
            phone_number = request.POST.get('phone_number')
            product_id = request.POST.get('product_id')
            
            phone_number = request.POST.get('phone_number')[1:]
            phone_number = re.sub('[^0-9]','', phone_number)

            code = generateCode()
            if Phone_numbers.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'Bu raqam allaqachon tasdiqlangan')
                return redirect('comp_rassom')
            verification_code = SmsPhoneVerify.objects.get_or_create(code=code, phone_number=phone_number, product_id=product_id)[0]

            try:
                send_sms(code, phone_number)
            except Exception as error:
                messages.error(request, str(error))
                return redirect('verify_rassom')
            
            return redirect('verify_rassom')
        context = {
            'rassom_comp':rassom_comp,
        }
        return render(request,'frontend/competition/rassom/comp_rassom.html', context)
    else:
        return redirect('timeout')
    

def VerifyRassom(request):
    counter_model = Counter.objects.get(id=1)
    datetime_object = datetime.datetime(counter_model.year, counter_model.month, counter_model.day)
    utc=pytz.UTC
    current_datetime = timezone.now() + timedelta(hours=5)
    expired_on = datetime_object.replace(tzinfo=utc)
    checked_on = current_datetime.replace(tzinfo=utc)
    if expired_on > checked_on and counter_model.competition == "Painting":
        rassom_comp = Comp_Rassom.objects.all()

        if request.method == 'POST':
            verify_code = request.POST.get('verify_code')

            try:
                verify_code_model = SmsPhoneVerify.objects.get(code = verify_code)
                utc=pytz.UTC
                current_datetime = timezone.now() + timedelta(hours=5)
                time = verify_code_model.publishing_date + timedelta(hours=5, minutes=1)
                expired_on = time.replace(tzinfo=utc)
                checked_on = current_datetime.replace(tzinfo=utc)
                if expired_on > checked_on:
                    Phone_numbers.objects.create(phone_number=verify_code_model.phone_number)
                    comp_product_detail = Comp_Rassom.objects.get(id=verify_code_model.product_id)
                    comp_product_detail.votes.add(Phone_numbers.objects.get(phone_number=verify_code_model.phone_number))
                    comp_product_detail.save()
                    
                    messages.success(request, 'Tasdiqlash muvaffaqiyatli amalga oshirildi')
                    return redirect('comp_rassom')
                else:
                    messages.error(request, 'Tasdiqlash kodi xato')
                    return redirect('verify_rassom')
            except SmsPhoneVerify.DoesNotExist:
                messages.error(request, 'Kutilmagan xato')
                return redirect('verify_rassom')
            finally:
                verify_code_model = get_object_or_none(SmsPhoneVerify, code = verify_code)
                if verify_code_model is None:
                    pass
                else:
                    verify_code_model.delete()
        context = {
            'rassom_comp':rassom_comp,
        }
        return render(request,'frontend/competition/rassom/verify_rassom.html', context)
    else:
        return redirect('timeout')
    
def TimeOut(request):
    return render(request,'frontend/pages/timeout.html')


class AuthCallbackView(View):
    def get(self, request):

        code = request.GET.get('code')

        # checking code
        if code is None:
            print("code mavjud emas!!!!!!")
            return

        # get access token and get user info
        client = oAuth2Client(
            client_id="6",
            client_secret="Lmf34scxVvECzfF4ljXAe7sIdVjJ1hO6nq6-7c7E",
            redirect_uri="https://24eb-195-158-14-110.ngrok-free.app/callback/",
            authorize_url="https://student.uzfi.uz/oauth/authorize",
            token_url="https://student.uzfi.uz/oauth/access-token",
            resource_owner_url="https://student.uzfi.uz/oauth/api/user?fields=id,uuid,type,name,login,picture,email,university_id,phone"
        )
        access_token_response = client.get_access_token(code)

        if 'access_token' in access_token_response:
            access_token = access_token_response['access_token']
            user_details = client.get_user_details(access_token)

            # get user
            try:
                user = CustomUser.objects.get(username=user_details['login'])
            except CustomUser.DoesNotExist:
                response = requests.get(user_details['picture'])

                # Ensure the request was successful
                if response.status_code == 200:
                    # Create a temporary file to store the downloaded image
                    img_temp = NamedTemporaryFile()
                    img_temp.write(response.content)
                    img_temp.flush()

                    # Create a Django File object
                    img_file = File(img_temp, name=user_details['picture'].split("/")[-1])

                    user = CustomUser(
                        username=user_details['login'], 
                        phone_number=user_details['phone'], 
                        profil_pic=img_file, 
                        user_type="USER")
                else:
                    user = CustomUser(username=user_details['login'], phone_number=user_details['phone'], user_type="USER")
            
                user.set_password(user_details['passport_number'])
                user.save()
            
            login(request, user)
            return redirect("talant_home")
            
        else:
            print("access_token mavjud emas!!!!!!!!")
            return redirect("index")
