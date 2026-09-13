from django.contrib import admin

# Register your models here.
from . models import Dados_Apontamentos
from import_export.admin import ImportExportActionModelAdmin

admin.site.register(Dados_Apontamentos, ImportExportActionModelAdmin)

