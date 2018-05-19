# Register your models here.
from django.contrib import admin
from .models import Museums, Selected, Comments, User_Page, Scored


admin.site.register(Museums)
admin.site.register(Selected)
admin.site.register(Comments)
admin.site.register(User_Page)
admin.site.register(Scored)