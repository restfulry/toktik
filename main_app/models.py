from django.db import models
from django.contrib.auth.models import User

CATEGORIES = (
    ('SCI', 'SCIENCE'),
    ('MAT', 'MATHEMATICS'),
    ('GAR', 'GARDEN'),
    ('OTH', 'OTHER')
)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    points = models.IntegerField(editable=False)


class Question(models.Model):
    question = models.CharField(max_length=500)
    category = models.CharField(
        max_length=3,
        choices=CATEGORIES,
    )
    is_anon = models.BooleanField(default=False)
    points = models.IntegerField(editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    # will need to implement video here
    answer = models.CharField(max_length=1)

    is_anon = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
