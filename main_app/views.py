from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import SignUpForm
from .models import Question, Member


class QuestionCreate(CreateView):
    model = Question
    fields = ['question', 'category']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['question', 'category']


class QuestionDelete(DeleteView):
    model = Question
    success_url = '/'


def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, 'main_app/question_detail.html', {'question': question})


def home(request):
    text = request.GET.get('text', '')
    return render(request, 'index.html', dict(text=text))


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


class ProfileUpdate(UpdateView):
    model = Member
    fields = ['email', 'first_name', 'last_name']
