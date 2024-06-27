from django.contrib import admin
from .models import *

admin.site.register(Award)
admin.site.register(About)
admin.site.register(DCUfmFamilyTree)

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)

admin.site.register(CommitteeMember)
admin.site.register(CommitteePage)
admin.site.register(GalleryPage)