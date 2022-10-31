from django.contrib import admin
from .models import *

class ArticleAdmin(admin.ModelAdmin):
    readonly_fields=('user','created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user_id=request.user.id

        obj.save()
# Register your models here.
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Like)



