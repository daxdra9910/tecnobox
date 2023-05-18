from django.contrib import admin
from django.contrib.auth.models import Group




admin.site.site_header = 'TecnoBox'
admin.site.site_title = 'TecnoBox'
admin.site.index_title = 'Panel de administración'


admin.site.unregister(Group)