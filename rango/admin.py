from django.contrib import admin

# Register your models here.
from rango.models import Category, Page, UserProfile

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_firlds = {'slug': ('name',)}
	
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)
admin.site.register(UserProfile)