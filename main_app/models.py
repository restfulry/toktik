from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

CATEGORIES = (
    ('SCI', 'SCIENCE'),
    ('MAT', 'MATHEMATICS'),
    ('GAR', 'GARDEN'),
    ('OTH', 'OTHER')
)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=150)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    points = models.IntegerField(editable=False, default='1000')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_member_signal(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)
    instance.member.save()


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
