from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import login, logout, authenticate
from .models import CustomUserManager, CustomUser, Question, Answer, Response
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.contrib import messages
import json
# Create your views here.
custom_user_manager = CustomUserManager()


def home(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect('questions')
        else:
            messages.info(request, 'Login to play the quiz')
            return redirect('login')
    return render(request, 'quiz_app/home.html')


@never_cache
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("user doesnt exist")
    return render(request, 'quiz_app/login.html')


def create(request):
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            username = request.POST.get('username')
            email = request.POST.get('email')
            User = get_user_model()
            user=CustomUser.objects.filter(username=username)
            if user is None:
                user = CustomUser.objects.create_user(
                username=username, password=password2, email=email)
            else:
                messages.warning(request,"User Already Exists")
            return redirect('login')
        else:
            messages.error(request,'password mismatched')
            return redirect('create')
    return render(request, 'quiz_app/create.html')


def show_questions(request):
    questions = Question.objects.prefetch_related('answers').order_by('id')
    question_per_page = 1
    paginator = Paginator(questions, question_per_page)
    request_page_no = request.GET.get('page')
    questions = paginator.get_page(request_page_no)
    print(questions)
    content = {
        'questions': questions,
    }
    return render(request, 'quiz_app/quiz.html', content)


def logout_user(request):
    logout(request)
    print(request.user)
    response = redirect('login')
    return response


def user_response(request):
    user = request.user
    data = json.loads(request.body)
    question_id = data['question_id']
    answer_selected = data['answer']
    question = Question.objects.get(id=question_id)
    response=Response.objects.create(user=user, question=question,
                            user_response=answer_selected)
    if answer_selected.strip().lower() == question.answer.strip().lower():
        response.status='Right answer'
        response.save()
        print(response.status)
        return JsonResponse('you selected the right answer',safe=False)
    else:
        response.status='Wrong answer'
        response.save()
        return JsonResponse('oops it was a wrong guess ',safe=False)
def my_responses(request):
    user=request.user
    responses=Response.objects.filter(user=user)
    content={'responses':responses}
    return render(request,'quiz_app/my_response.html',content)
def exit_game(request):
    messages.success(request,f"Thanks for playing this quiz  {request.user}")
    return redirect('home')