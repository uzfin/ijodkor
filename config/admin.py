from django.contrib import admin
from .models import CustomUser, TalandCategory, Artists, Managers, Sher, LikeID, UnLikeID, Rassom, Image, Videos, Song, Counter, Comp_Song, Phone_numbers, SmsPhoneVerify, Comp_Video, Comp_Sher, Comp_Image, Comp_Rassom
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from django.db.models import Q


class CustomUserAdmin(admin.ModelAdmin):
       list_display = ('username', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active', "phone_number")
       list_filter = ('is_staff', 'is_active')
       search_fields = ('username', 'first_name', 'last_name')
       ordering = ('username',)
       filter_horizontal = ()
       fieldsets = (
           (None, {'fields': ('username', 'password')}),
           ('Personal Info', {'fields': ('first_name', 'last_name')}),
           ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
           ('Important dates', {'fields': ('last_login', 'date_joined')}),
       )
admin.site.register(CustomUser, CustomUserAdmin)

class TalandCategoryAdmin(admin.ModelAdmin):
        list_display = ('name', "whofrom", "user_type_name", "created_at")
        search_fields = ('name', "whofrom__user_type", "whofrom__username")
admin.site.register(TalandCategory, TalandCategoryAdmin)



class ArtistAdmin(admin.ModelAdmin):
    list_display = ('artist', 'phone_number', 'created_at')
admin.site.register(Artists, ArtistAdmin)

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('manager', 'created_at')
admin.site.register(Managers, ManagerAdmin)

class SherAdmin(admin.ModelAdmin):
#     list_filter = ['situation', ]
    list_display = ['id', 'title', 'created_at', 'status', '_']
    search_fields = ['title', 'status']
    list_per_page = 10

    def _(self, obj):
        if obj.situation == 'Active':
            return True
        else:
            return False
    _.boolean = True

    # Function to color the text (Active - Inactive)
    def status(self, obj):
        if obj.situation == 'Active':
            color = '#28a745'
        else:
            color = 'red'
        return format_html('<strong><p style="color: {}">{}</p></strong>'.format(color, obj.situation))

    status.allow_tags = True
admin.site.register(Sher, SherAdmin)



class VideosAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', "videofile", 'created_at', 'status', '_']
    search_fields = ['title', 'status']
    list_per_page = 10

    def _(self, obj):
        if obj.situation == 'Active':
            return True
        else:
            return False
    _.boolean = True

    # Function to color the text (Active - Inactive)
    def status(self, obj):
        if obj.situation == 'Active':
            color = '#28a745'
        else:
            color = 'red'
        return format_html('<strong><p style="color: {}">{}</p></strong>'.format(color, obj.situation))

    status.allow_tags = True
admin.site.register(Videos, VideosAdmin)


class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'song_title', "audio_file", 'created_at', 'status', '_']
    search_fields = ['title', 'status']
    list_per_page = 10

    def _(self, obj):
        if obj.situation == 'Active':
            return True
        else:
            return False
    _.boolean = True

    # Function to color the text (Active - Inactive)
    def status(self, obj):
        if obj.situation == 'Active':
            color = '#28a745'
        else:
            color = 'red'
        return format_html('<strong><p style="color: {}">{}</p></strong>'.format(color, obj.situation))

    status.allow_tags = True
admin.site.register(Song, SongAdmin)

class ImageInline(admin.TabularInline):
    model = Image


class RassomAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
admin.site.register(Rassom, RassomAdmin)


class CompImageInline(admin.TabularInline):
    model = Comp_Image


class CompRassomAdmin(admin.ModelAdmin):
    inlines = [
        CompImageInline,
    ]
admin.site.register(Comp_Rassom, CompRassomAdmin)

admin.site.register(LikeID)
admin.site.register(UnLikeID)
admin.site.register(Counter)
admin.site.register(Comp_Song)
admin.site.register(Comp_Video)
admin.site.register(Comp_Sher)
admin.site.register(Phone_numbers)
admin.site.register(SmsPhoneVerify)



