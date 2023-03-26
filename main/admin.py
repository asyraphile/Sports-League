from django.contrib import admin
from . models import Team, User, Upload, Match
# Register your models here.
admin.site.register(Team)
admin.site.register(User)
admin.site.register(Upload)
admin.site.register(Match)