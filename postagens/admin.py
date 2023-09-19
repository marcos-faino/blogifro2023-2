from django.contrib import admin
from .models import Postagem


@admin.register(Postagem)
class PostagemAdmin(admin.ModelAdmin):
    list_display = ['autor','titulo', 'criado', 'status']
    list_editable = ['status']
    prepopulated_fields = {'slug':('titulo',)}
    ordering = ('-status', 'criado')

