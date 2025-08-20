from django.contrib import admin
from .models import Comment, Post, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'last_modified', 'has_media')
    list_filter = ('created_on', 'last_modified', 'categories', 'media_type')
    search_fields = ('title', 'body')
    filter_horizontal = ('categories',)
    fields = ('title', 'body', 'categories', 'media_file')
    
    def has_media(self, obj):
        return bool(obj.media_file)
    has_media.short_description = "Tiene archivo"
    has_media.boolean = True

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_on')
    list_filter = ('created_on', 'post')
    search_fields = ('author', 'body')
    fields = ('author', 'post', 'body')