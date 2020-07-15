from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # displayed fields on the post list page
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    # searchbar
    search_fields = ('title', 'body')
    # populates slug field whenever something is written in title field
    prepopulated_fields = {'slug': ('title',)}
    # author field has lookup and authors can be searched by their id or name
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
