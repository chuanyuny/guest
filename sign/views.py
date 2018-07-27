from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,get_object_or_404


def index(request):
    return render(request,"index.html")

def login_action(request):
    if request.method =='POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            #response.set_cookie('user',username,3600)
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})

@login_required
def event_manage(request):
    #username = request.COOKIES.get('user','')
    event_list = Event.objects.all()
    username = request.session.get('user','')
    return render(request,"event_manage.html",{"user":username,"events":event_list})

@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name',"")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,"event_manage.html",{"user":username,"events":event_list})

@login_required
def guest_manage(request):
    username = request.session.get('user','')
    guest_list=Guest.objects.all()
    paginator=Paginator(guest_list,2)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator.num_pages)
    return render(request,"guest_manage.html",{"user":username,"guests":contacts})

@login_required
def user_search_name(request):
    username = request.session.get('user','')
    user_search_name = request.GET.get('realname',"")
    guest_list = Guest.objects.filter(realname__contains=user_search_name)
    paginator=Paginator(guest_list,2)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator.num_pages)
    return render(request,"guest_manage.html",{"user":username,"guests":contacts})

@login_required
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)
    person_sum=len(Guest.objects.filter(event=event))
    has_signed_num=len(Guest.objects.filter(event=event,sign=True))
    return render(request,'sign_index.html',{'event':event,'people_num':person_sum,'has_signed_num':has_signed_num})

@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event,id=eid)
    phone = request.POST.get('phone','')
    print phone
    person_sum = len(Guest.objects.filter(event=event))
    has_signed_num = len(Guest.objects.filter(event=event, sign=True))
    result =Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error.','people_num':person_sum,'has_signed_num':has_signed_num})

    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':"event id or phone error.",'people_num':person_sum,'has_signed_num':has_signed_num})

    result=Guest.objects.get(phone=phone,event_id=eid)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':"user has sign in.",'people_num':person_sum,'has_signed_num':has_signed_num})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        has_signed_num = has_signed_num+1
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success!','guest':result,'people_num':person_sum,'has_signed_num':has_signed_num})

@login_required
def logout(request):
    auth.logout(request)
    response=HttpResponseRedirect('/index/')
    return response

























