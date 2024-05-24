from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ImageOfUsers)
admin.site.register(AboutOfUsers)
admin.site.register(Friendship)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Notification)
