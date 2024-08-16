from django.contrib import admin
from . import models
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug': ('name',)}
    list_display = ['name','slug']

admin.site.register(models.bookCategory,CategoryAdmin)
admin.site.register(models.BookModel)
admin.site.register(models.BorrowModel)
admin.site.register(models.ReturnModel)
admin.site.register(models.CommentModel)