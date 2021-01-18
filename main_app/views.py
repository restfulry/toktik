from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import SignUpForm, QuestionForm
from .models import Question, Member, Answer, Photo, Like
import uuid
import boto3
from .forms import AnswerForm

# AWS Base URL and S3 Bucket
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'toktikproject'


class QuestionCreate(CreateView):
    model = Question
    form_class = QuestionForm
    # fields = ['question', 'category', 'is_anon']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['question', 'category']


class QuestionDelete(DeleteView):
    model = Question
    success_url = '/'


def questions_index(request):
    questions = Question.objects.all()
    return render(request, 'questions/index.html', {'questions': questions})


def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    answer_form = AnswerForm()
    return render(request, 'main_app/question_detail.html', {'question': question, 'answer_form': answer_form})


def questions_sort(request, category):
    print(f"{category}")
    questions = Question.objects.filter(category=category)
    return render(request, 'questions/index.html', {'questions': questions})


def home(request):
    text = request.GET.get('text', '')
    questions = Question.objects.all()
    answers = Answer.objects.all()
    return render(request, 'index.html', {'text': text, 'questions': questions, 'answers': answers, 'form': QuestionForm})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.member.first_name = form.cleaned_data.get('first_name')
            user.member.last_name = form.cleaned_data.get('last_name')
            user.member.email = form.cleaned_data.get('email')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = SignUpForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def profile_detail(request, member_id):
    member = Member.objects.get(id=member_id)
    return render(request, 'profile/detail.html', {
        'member': member
    })


def add_answer(request, question_id):
    form = AnswerForm(request.POST)
    if form.is_valid():
        new_answer = form.save(commit=False)
        new_answer.question_id = question_id
        new_answer.user_id = request.user.id
        new_answer.save()
    return redirect('question_detail', question_id=question_id)


def like_answer(request):
    user = request.user
    if request.method == 'POST':
        answer_id = request.POST.get('answer_id')
        answer = Answer.objects.get(id=answer_id)

        if user in answer.liked.all():
            answer.liked.remove(user)
        else:
            answer.liked.add(user)

        like, created = Like.objects.get_or_create(
            user=user, answer_id=answer_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
    return redirect('home')


class ProfileUpdate(UpdateView):
    model = Member
    fields = ['email', 'first_name', 'last_name']


def change_photo(request, member_id):
    member = Member.objects.get(id=member_id)
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            print("test1")
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            print("test2")
            photo = Photo(url=url, member_id=member_id)
            print("test3")
            photo.save()
            print("test4")
            return redirect('profile_detail', member_id=member_id)
            print("test5")
        except:
            print('An error occurred uploading file to S3')
    return render(request, 'main_app/picture_upload.html', {
        'member': member,
    })
