from django.contrib import admin

from applications.events.models import Events, Image

admin.site.register(Events)
admin.site.register(Image)
