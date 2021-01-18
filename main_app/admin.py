from django.contrib import admin
from .models import Member, Answer, Question, Photo, Like_Answer, Like_Question

# Register your models here.
admin.site.register(Member)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Like_Answer)
admin.site.register(Like_Question)
admin.site.register(Photo)
