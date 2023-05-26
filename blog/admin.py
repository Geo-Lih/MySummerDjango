from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'updated_on', 'content', 'status']
    prepopulated_fields = {'slug': ('title',)}
    actions = ['set_status']
    list_filter = ['status']
    search_fields = ['title']

    @admin.action(description='Publish post')
    def set_status(self, request, queryset):
        res = queryset.update(status=1)
        return self.message_user(request, f'{res} posts wast published')


