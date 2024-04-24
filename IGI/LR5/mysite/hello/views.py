from django.shortcuts import render
from django.http import HttpResponse,HttpResponsePermanentRedirect,HttpResponseRedirect,HttpResponseForbidden
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

def json(request):
    bob = Person("Bob", 41)
    return JsonResponse(bob, safe=False, encoder=PersonEncoder)

class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

class PersonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Person):
            return {"name": obj.name, "age": obj.age}
            # return obj.__dict__
        return super().default(obj)
# Create your views here.


def index(request):
    return HttpResponse("Hello METANIT.COM")

def profile(request,name,age):
    username = request.COOKIES["username"]
    return HttpResponse(f'''
                        <h2> О пользователе </h2>
                        <p> Имя: {name} ({username}) </p>
                        <p> Возраст: {age} </p>
                        ''')

def about(request,name="Pog",age=228):
    user_agent = request.META["HTTP_USER_AGENT"]
    user_ip = request.META["REMOTE_ADDR"]
    if age == 101:
        return HttpResponseForbidden("Забанен")
    return HttpResponse(f'''
                        <h2> О пользователе </h2>
                        <p> Имя: {name} </p>
                        <p> Возраст: {age} </p>
                        <p> Браузер: {user_agent} </p>
                        <p> IP: {user_ip} </p>
                        ''')

def stats(request):
        age = request.GET.get("age",12) #передаем через url
        name = request.GET.get("name","Min")
        return HttpResponse(f"<h2>Имя: {name}  Возраст: {age}</h2>")
def contact(request):
    header = "Данные пользователя"              # обычная переменная
    langs = ["Python", "Java", "C#"]            # список
    user = {"name" : "Tom", "age" : 23}          # словарь
    address = ("Абрикосовая", 23, 45)           # кортеж

    data = {"header": header, "langs": langs, "user": user, "address": address}
    return render(request,"contact.html",context=data)


def new(request):
    return HttpResponse("Новый пользователь")

def old(request):
    return HttpResponseRedirect("/stats")

def home(request):
    return HttpResponsePermanentRedirect("/")

def set(request):
    username = request.GET.get("username","Empty")
    response = HttpResponse(f"Привет {username}")
    response.set_cookie("username",username)
    return response

def get(request):
    username = request.COOKIES["username"]
    return HttpResponse(f"Пока {username}")
