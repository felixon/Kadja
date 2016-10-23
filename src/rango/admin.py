from django.contrib import admin
from rango.models import Category, Page, UserProfile, Post, Article
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'picture', 'published', 'status')
    list_filter = ('status', 'created', 'published', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields ={'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published'
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
class PageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'url', 'views')
    list_filter = ('views', 'url')
    search_fields = ('title', 'url')
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website', 'picture')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Article)


