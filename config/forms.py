from django import forms
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
from .models import Sher, Videos, Song
from django import forms
from django.forms import inlineformset_factory
from django.contrib import messages



from .models import (
    Rassom, Image
)

class SherForm(forms.ModelForm):
    class Meta:
        model = Sher
        fields = ['title', 'text']
        widgets = {
            'title':forms.TextInput(attrs={"class":"form-control"}),
            'text':forms.TextInput(attrs={"class":"form-control"})
        }
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     title = cleaned_data.get("title")
    #     if Sher.objects.filter(title=title).exists():
    #         # messages.warning(self.request, "Xato ")
    #         raise forms.ValidationError(str(title) + ' is already created')
    #     return super().clean()

class VideoForm(forms.ModelForm):
    class Meta:
        model= Videos
        fields= ["title", "videofile"]
        widgets = {
            'title':forms.TextInput(attrs={"class":"form-control"})
        }
    


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']
        widgets = {
            'song_title':forms.TextInput(attrs={"class":"form-control"}),
        }

class RassomForm(forms.ModelForm):

    class Meta:
        model = Rassom
        fields = ['title', 'img']
    
        widgets = {
            'title':forms.TextInput(attrs={"class":"form-control"})
        }



class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = '__all__'



ImageFormSet = inlineformset_factory(
    Rassom, Image, form=ImageForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)
