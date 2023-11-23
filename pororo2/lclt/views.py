from .models import Room,Notice
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect,  resolve_url
from django.utils import timezone
from django.template import RequestContext
#from .forms import QuestionForm, AnswerForm
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import UserForm , RoomForm
from .any import generate_random_string
from django.core.paginator import Paginator  
from django.contrib.auth.decorators import login_required
from django.views import generic


# Create your views here.

def index(request):
    # user가 로그인 됬을때 user의 역참조를 이용해서 방의 리스트를 보냄
    notice_list = Notice.objects.order_by('-create_date')[:5]
    if request.user.is_authenticated:
        room_list = Room.objects.filter(users=request.user).order_by('-create_date')[:5]
        print(room_list)
        context = {'room_list': room_list, 'notice_list': notice_list}
    else:
        context = {'notice_list': notice_list}
    return render(request, 'lclt/main.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user1 = authenticate(username = username, password = raw_password)
            login(request,user1)
            return redirect('/')
        else:
            return render(request, 'lclt/signup.html',{"formd" : form })
    else:
        form = UserForm()
    return render(request, 'lclt/signup.html')

@login_required(login_url='lclt:login')
def myuser(request,user_id):
    return render(request,'lclt/myuser.html')

@login_required(login_url='lclt:login')
def room_make(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        form.fields['users'].queryset = User.objects.filter(pk__in=request.POST.getlist('users'))
        if form.is_valid():
            users = form.cleaned_data['users']
            room = form.save(commit = False)
            chekcer = generate_random_string()
            while Room.objects.filter(code=chekcer).exists():
                chekcer = generate_random_string()
            room.code = chekcer
            room.create_date = timezone.now()
            room.save()
            room.users.set(users)
            return redirect('/')
        else:
            user_list = User.objects.order_by('username')
            context = {'user_list' : user_list , 'form' : form}
            return render(request,'lclt/room_make.html',context)        
    user_list = User.objects.order_by('username')
    context = {'user_list' : user_list}
    return render(request,'lclt/room_make.html',context)

@login_required(login_url='lclt:login')
def allroom(request):
    room_list = Room.objects.filter(users=request.user).order_by('-create_date')
    for room in room_list:
        room.datediff = (timezone.now()-room.create_date).days
    return render(request,'lclt/allroom.html',{'room_list' : room_list})

def notice(request):
    page = request.GET.get('page', '1')
    notice_list = Notice.objects.order_by('-create_date')
    paginator = Paginator(notice_list, 10)
    page_obj = paginator.get_page(page)
    context = {'notice_list': page_obj}
    return render(request,'lclt/notice.html',context)

def notice_detail(request,notice_id):
    notice = get_object_or_404(Notice,pk = notice_id)
    return render(request,'lclt/notice-detail.html',{'notice' : notice})

@login_required(login_url='lclt:login')
def roomcam(request,code_id):
    myroom = get_object_or_404(Room,code = code_id)
    if request.user.username in myroom.users.values_list('username', flat=True):
        return render(request,'lclt/roomcam.html',{'code_id' : code_id,'room' : myroom})
    else:
        return render(request, 'lclt/403.html', status=403)

@login_required(login_url='lclt:login')    
def room_modify(request,code_id):
    myroom = get_object_or_404(Room,code = code_id)
    if request.user.username in myroom.users.values_list('username', flat=True):
        if request.method == "POST":
            form = RoomForm(request.POST, request.FILES,instance=myroom)
            form.fields['users'].queryset = User.objects.filter(pk__in=request.POST.getlist('users'))
            if form.is_valid():
                users = form.cleaned_data['users']
                room = form.save(commit=False)
                room.save()
                room.users.set(users)
                return redirect('/allroom')
        else:
            room_users = list(myroom.users.all())
            print(room_users)
            return render(request,'lclt/room_edit.html',{'code_id' : code_id,'room' : myroom,'user_list' : User.objects.order_by('username'),'room_users' : room_users})
    else:
        return render(request, 'lclt/403.html', status=403)
    

def delete_room(request, code_id):
    print(1)
    room = get_object_or_404(Room, code=code_id)
    room.delete()
   
    
    
