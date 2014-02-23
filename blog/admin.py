from django.contrib import admin
from Metten.blog.models import Post, Links, Best, Search

admin.site.register(Post)
admin.site.register(Links)
admin.site.register(Best)
admin.site.register(Search)
#takes care of admin.PY and models