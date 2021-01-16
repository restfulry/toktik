from django.contrib import admin
from .models import Member, Answer, Question, Photo

# Register your models here.
admin.site.register(Member)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Photo)
