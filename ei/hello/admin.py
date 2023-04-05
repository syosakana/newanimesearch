from django.contrib import admin
from .models import Anime,Message,Friend,Good,WhoGood

# Register your models here.

admin.site.register(Anime)
admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(Good)
admin.site.register(WhoGood)