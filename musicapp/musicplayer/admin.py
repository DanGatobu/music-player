from django.contrib import admin

from .models import audio,favorite,test
# Register your models here.
admin.site.register(audio)
admin.site.register(favorite)
admin.site.register(test)