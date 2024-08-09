from  django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Sher, Artists, Rassom, Videos, Song
from django.contrib import messages
from .forms import SherForm, RassomForm, VideoForm, SongForm


from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)

from .forms import (
    RassomForm, ImageFormSet
)
from .models import (
    Image,
    Rassom
)



@login_required(login_url='login')
def talant_home(request):
    ctx = {
        "user": request.user
    }
    return render(request, 'backend/Talant/index.html', ctx)

# ==================================== SHER ======================================
@login_required(login_url='login')
def ADD_SHER(request):
    for i in request.user.artists.taland_category.all():
        if i.name == "She'r":
            if request.method == 'POST':
                form = SherForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    talant = Artists.objects.get(artist = request.user)
                    sher = Sher(
                        user=talant,
                        title=cd['title'],
                        text=cd['text'],
                        situation='Inactive'
                    )
                    sher.save()
                messages.success(request, "Siz yuklagan she'r muvaffaqiyatli qo'shildi")
                return redirect('view_sher')
            else:
                form = SherForm()
            context = {
                'form':form
            }
            return render(request, 'backend/Talant/pages/sher/add_sher.html', context)
    return redirect('talant_home')

@login_required(login_url='login')
def VIEW_SHER(request):
    for i in request.user.artists.taland_category.all():
        if i.name == "She'r":
            artist = Artists.objects.get(artist=request.user)
            shers = Sher.objects.filter(user=artist, deleted=False)

            context = {
                'shers':shers
            }
            return render(request, 'backend/Talant/pages/sher/view_sher.html', context)
    return redirect('talant_home')

@login_required(login_url='login')
def SherDetailView(request, pk):
    for i in request.user.artists.taland_category.all():
        if i.name == "She'r":
            object = Sher.objects.get(id=pk)
            context = {
                'object':object,
            }
            return render(request, 'backend/Talant/pages/sher/each_sher_view.html', context)
    return redirect('talant_home')

@login_required(login_url='login')
def EditSher(request, pk):
    for i in request.user.artists.taland_category.all():
        if i.name == "She'r":
            sher = Sher.objects.get(id=pk)
            if request.method == 'GET':
                context = {'form': SherForm(instance=sher)}
                return render(request,'backend/Talant/pages/sher/edit_sher.html',context)
            
            elif request.method == 'POST':
                form = SherForm(request.POST, instance=sher)
                if form.is_valid():
                    text = form.cleaned_data['text']
                    form.save()
                    messages.success(request, "She'r muvaffaqiyatli yangilandi")
                    return redirect('view_sher')
                else:
                    messages.error(request, 'Xatolik yuzaga keldi')
                    return render(request,'backend/Talant/pages/sher/edit_sher.html',{'form':form})
    return redirect('talant_home')
   
@login_required(login_url='login')
def DeleteSher(request, pk):
    for i in request.user.artists.taland_category.all():
        if i.name == "She'r":
            sher = Sher.objects.get(id=pk)
            sher.deleted=True
            sher.save()
            messages.success(request, "Sher muvaffaqiyatli o'chirildi")
            return redirect('view_sher')
    return redirect("talant_home")


def Active_Sher(request, pk):
    sher = Sher.objects.get(id=pk)
    sher.situation="Active"
    sher.save()
    messages.success(request, "She'r activlashtirildi")
    return redirect('view_sher')

def InActive_Sher(request, pk):
    sher = Sher.objects.get(id=pk)
    sher.situation="Inactive"
    sher.save()
    messages.success(request, "She'r faol emas")
    return redirect('view_sher')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================== Videos ========================================
def ADD_VIDEO(request):
    for i in request.user.artists.taland_category.all():
        if i.name == "Video":
            if request.method == 'POST':
                form = VideoForm(request.POST, request.FILES)
                if form.is_valid():
                    cd = form.cleaned_data
                    talant = Artists.objects.get(artist = request.user)
                    video = Videos(
                        user=talant,
                        title=cd['title'],
                        videofile=cd['videofile'],
                        situation='Inactive'
                    )
                    video.save()
                messages.success(request, "Siz yuklagan video muvaffaqiyatli qo'shildi")
                return redirect('list_video')
            else:
                form = VideoForm()
            context = {
                'form':form
            }
            return render(request, 'backend/Talant/pages/video/add_video.html', context)
    return redirect('talant_home')

def LIST_VIDEOS(request):
    for i in request.user.artists.taland_category.all():
        if i.name == "Video":
            artist = Artists.objects.get(artist=request.user)
            videos = Videos.objects.filter(user=artist, deleted=False)

            context = {
                'videos':videos
            }
            return render(request, 'backend/Talant/pages/video/list_video.html', context)
    return redirect('talant_home')

def VideoDetailView(request, pk):
    for i in request.user.artists.taland_category.all():
        if i.name == "Video":
            object = Videos.objects.get(id=pk)
            context = {
                'object':object,
            }
            return render(request, 'backend/Talant/pages/video/each_video_view.html', context)
    return redirect('talant_home')

def EditVideo(request, pk):
    for i in request.user.artists.taland_category.all():
        if i.name == "Video":
            video = Videos.objects.get(id=pk)
            if request.method == 'GET':
                context = {'form': VideoForm(instance=video)}
                return render(request,'backend/Talant/pages/video/edit_video.html', context)
            
            elif request.method == 'POST':
                form = VideoForm(request.POST, request.FILES, instance=video)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'The post has been updated successfully.')
                    return redirect('list_video')
                else:
                    messages.error(request, 'Please correct the following errors:')
                    return render(request,'backend/Talant/pages/video/edit_video.html',{'form':form})
    return redirect('talant_home')
        
def DeleteVideo(request, pk):
    for i in request.user.artists.taland_category.all():
        if i.name == "Video":
            video = Videos.objects.get(id=pk)
            video.deleted=True
            video.save()
            messages.success(request, "Video muvaffaqiyatli o'chirildi")
            return redirect('list_video')
    return redirect('talant_home')


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ================================== RASSOM ========================================
class RassomInline():
    
    form_class = RassomForm
    model = Rassom
    template_name = "backend/Talant/pages/rassom/rassom_create_or_update.html"

    def form_valid(self, form):
        for i in self.request.user.artists.taland_category.all():
            if i.name == "Rasm":
                named_formsets = self.get_named_formsets()
                if not all((x.is_valid() for x in named_formsets.values())):
                    return self.render_to_response(self.get_context_data(form=form))
                
                self.object = form.save()
                talant = Artists.objects.get(artist = self.request.user)
                self.object.user = talant
                self.object = form.save()

                # for every formset, attempt to find a specific formset save function
                # otherwise, just save.
                for name, formset in named_formsets.items():
                    formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
                    if formset_save_func is not None:
                        formset_save_func(formset)

                    else:
                        formset.save()
                return redirect('list_rassoms')
        return redirect('talant_home')


    def formset_images_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        images = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.rassom = self.object
            image.save()


class RassomCreate(RassomInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(RassomCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'images': ImageFormSet(prefix='images'),
            }
        else:
            return {
                'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }

    
class RassomUpdate(RassomInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(RassomUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }


def delete_image(request, pk):
    try:
        image = Image.objects.get(id=pk)
    except Image.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('update_rassom', pk=image.rassom.id)

    image.delete()
    messages.success(
            request, 'Image deleted successfully'
            )
    return redirect('update_rassom', pk=image.rassom.id)


class RassomList(ListView):
    model = Rassom
    template_name = "backend/Talant/pages/rassom/rassom_list.html"
    context_object_name = "rassoms"

    def get_queryset(self):
        return Rassom.objects.filter(deleted=False)

def RassomDetailView(request, pk):
    for i in request.user.artists.taland_category.all():
        if i.name == "Rasm":
            object = Rassom.objects.get(id=pk)
            context = {
                'object':object,
            }
            return render(request, 'backend/Talant/pages/rassom/each_rassom_view.html', context)
    return redirect('talant_home')


def DeleteRassom(request, pk):
    for i in request.user.artists.taland_category.all():
        if i.name == "Rasm":
            rassom = Rassom.objects.get(id=pk)
            rassom.deleted=True
            rassom.save()
            messages.success(request, "Rassom muvaffaqiyatli o'chirildi")
            return redirect('list_rassoms')
    return redirect('talant_home')

# -==-=--=-=-=-=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=-==--=-=-=-==-=-=-==---==-=-=-=-=--=


# ================================== SONG ========================================
def ADD_SONG(request):
    for i in request.user.artists.taland_category.all():
        if i.name == "Qo'shiq":
            if request.method == 'POST':
                form = SongForm(request.POST, request.FILES)
                if form.is_valid():
                    cd = form.cleaned_data
                    talant = Artists.objects.get(artist = request.user)
                    video = Song(
                        user=talant,
                        song_title=cd['song_title'],
                        audio_file=cd['audio_file'],
                        situation='Inactive'
                    )
                    video.save()
                messages.success(request, "Siz yuklagan Song muvaffaqiyatli qo'shildi")
                return redirect('list_song')
            else:
                form = SongForm()
            context = {
                'form':form
            }
            return render(request, 'backend/Talant/pages/song/add_song.html', context)
    return redirect('talant_home')

def LIST_SONGS(request):
    for i in request.user.artists.taland_category.all():
        if i.name == "Qo'shiq":
            artist = Artists.objects.get(artist=request.user)
            songs = Song.objects.filter(user=artist, deleted=False)

            context = {
                'songs':songs
            }
            return render(request, 'backend/Talant/pages/song/list_song.html', context)
    return redirect('talant_home')

def SongDetailView(request, pk):
    for i in request.user.artists.taland_category.all():
        if i.name == "Qo'shiq":

            object = Song.objects.get(id=pk)
            context = {
                'object':object,
            }
            return render(request, 'backend/Talant/pages/song/each_song_view.html', context)
    return redirect('talant_home')

def EditSong(request, pk):
    for i in request.user.artists.taland_category.all():
        if i.name == "Qo'shiq":
            video = Song.objects.get(id=pk)
            if request.method == 'GET':
                context = {'form': SongForm(instance=video)}
                return render(request,'backend/Talant/pages/song/edit_song.html', context)
            
            elif request.method == 'POST':
                form = SongForm(request.POST, request.FILES, instance=video)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Qo'shiq muvaffaqiyatli yangilandi")
                    return redirect('list_song')
                else:
                    messages.error(request, 'Xatolik yuz berdi')
                    return render(request,'backend/Talant/pages/song/edit_song.html',{'form':form})
    return redirect('talant_home')
        
def DeleteSong(request, pk):
    for i in request.user.artists.taland_category.all():
        if i.name == "Qo'shiq":
            song = Song.objects.get(id=pk)
            song.deleted=True
            song.save()
            messages.success(request, "Song muvaffaqiyatli o'chirildi")
            return redirect('list_song')
    return redirect('talant_home')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=