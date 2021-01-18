from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

CATEGORIES = (
    ('SCI', 'SCIENCE'),
    ('MAT', 'MATHEMATICS'),
    ('GAR', 'GARDEN'),
    ('OTH', 'OTHER')
)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
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

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'member_id': self.id})


class Question(models.Model):
    question = models.CharField(max_length=500)
    category = models.CharField(
        max_length=3,
        choices=CATEGORIES,
    )
    is_anon = models.BooleanField(default=False)
    points = models.IntegerField(default='1000')
    liked = models.ManyToManyField(
        User, default=None, blank=True, related_name='liked_question')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"question_id": self.id})

    @property
    def num_likes(self):
        return self.liked.all().count()


class Answer(models.Model):
    # will need to implement video here
    answer = models.URLField(max_length=400)

    is_anon = models.BooleanField(default=False)
    points = models.IntegerField(default='1000')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    liked = models.ManyToManyField(
        User, default=None, blank=True, related_name='liked')

    def __str__(self):
        return self.answer

    @property
    def num_likes(self):
        return self.liked.all().count()


class Like_Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=True)
    value = models.CharField(choices=LIKE_CHOICES,
                             default='Like', max_length=10)

    def __str__(self):
        return str(self.answer)


class Like_Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=True)
    value = models.CharField(choices=LIKE_CHOICES,
                             default='Like', max_length=10)

    def __str__(self):
        return str(self.answer)


class Photo(models.Model):
    url = models.CharField(max_length=200)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for member_id: {self.member_id} @{self.url}"
