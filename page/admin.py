from django.contrib import admin

# Register your models here.
from page.models import Tag, Page, Post

admin.site.register(Tag)
admin.site.register(Page)
admin.site.register(Post)