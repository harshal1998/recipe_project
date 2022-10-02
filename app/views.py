from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import logout
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def registration(request):
    if request.method == 'POST':
        print("post")
        try:
            name = request.POST['name']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            print("details",name,email,username,password)
            User.objects.create(name=name,username=username, email=email, password=password)
            return redirect("/login")
        except Exception as e:
            print(e)
            return redirect("/registration")
    return render(request,"registration.html")


def login(request):
    if 'is_authenticated' in request.session:
        return redirect("/home")
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            print(username,password)
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                print("check password",check_password(user.password, password))
                if check_password(password,user.password):
                    request.session['is_authenticated'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_username'] = user.username
                    messages.success(request, f"{user.username} Logged in successfully." )
                    return redirect('/')
                else:
                    messages.error(request, "Invalid Credentials" )
                    return redirect("/login")
            else:
                messages.info(request, "User does not exists")
                return redirect("/login")
        except Exception as e:
            print(e)
            return redirect("/registartion")
    return render(request,"login.html")


def logout(request):
   request.session.flush()
   return redirect("/login")

def home(request):
    if 'is_authenticated' in request.session:
        page = request.GET.get("page")
        data_qr = Receipies.objects.all().order_by('-id')
        paginator = Paginator(data_qr, 6)
        if page == None:
            page = "1"
        data = paginator.get_page(page)
        return render(request,"home.html",context={'data':data,"page_no":str(page)})
    return redirect("/login")


def recipe_detail(request,id):
    data = Receipies.objects.get(id=id)
    return render(request,"recipe.html",context={'data':data})


class add_recipe(View):
    def get(self,request):
        return render(request,"add.html")

    def post(self,request):
        try:
            name = request.POST['name']
            image = request.FILES['image']
            description = request.POST['description']
            ingredients = request.POST['ingredients']
            recipe = request.POST['recipe']
            # request.FILES[]
            user = User.objects.get(id=request.session['user_id'])
            a = Receipies.objects.create(
                name=name,
                image=image,
                description=description,
                ingredients=ingredients,
                recipe=recipe,
                added_by=user
            )
            messages.success(request, f"{a.name} recipe added successfully")
            return redirect("/add")
        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong")
            return redirect("/add")

    

class edit_recipe(View):
    def get(self, request,id):
        data = Receipies.objects.get(id=id)
        return render(request,"edit.html",context={'data':data})

    def post(self,request,id):
        try:
            name = request.POST['name']
            image = request.FILES.get('image')
            description = request.POST['description']
            ingredients = request.POST['ingredients']
            recipe = request.POST['recipe']
            a = Receipies.objects.get(id=id)
            a.name=name
            if image != None:
                a.image=image
            a.description=description
            a.ingrediants=ingredients
            a.recipe=recipe
            a.save()
            messages.success(request, f"{a.name} recipe edited successfully")
            return redirect("/")
        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong")
            return redirect("/")


def view_recipe(request,id):
    data = Receipies.objects.get(id=id)
    return render(request,"view.html",context={"data":data})


def search(request):
    try:
        keyword = request.GET.get('keyword')
        # print("keyword",keyword)
        if keyword == "":
            return redirect("/")
        data = Receipies.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword) | Q(ingredients__icontains=keyword) | Q(recipe__icontains=keyword))
        # print(data)
        return render(request,"home.html",context={'data':data})
    except Exception as e:
        print(e)
        return redirect("/")