from django.shortcuts import render,redirect

# Create your views here.
from django import forms
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from myapp.models import Cake
class CakeForm(forms.ModelForm):
    class Meta:
        model=Cake
        fields="__all__"
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "flavour":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "shape":forms.TextInput(attrs={"class":"form-control"}),
            "weight":forms.TextInput(attrs={"class":"form-control"}),
            "layer":forms.NumberInput(attrs={"class":"form-control"}),
            "pic":forms.FileInput(attrs={"class":"form-control"}),
        }
class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            
        }
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
class CakeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=CakeForm()
        return render(request,"cake-add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=CakeForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"cake has been created successfully")
            return redirect("cake-list")
        messages.error(request,"cake not created")
        return render(request,"cake-add.html",{"form":form})
class CakeListView(View):
    def get(self,request,*args,**kwargs):
        qs=Cake.objects.all()
        return render(request,"cake-list.html",{"cake":qs})
class CakeDetailView(View):
    def get(self,request,*args,**kwargs):
       
        id=kwargs.get("pk")
        qs=Cake.objects.get(id=id)
        return render(request,"cake-detail.html",{"cake":qs})
class CakeEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp=Cake.objects.get(id=id)
        form=CakeForm(instance=emp)
        return render(request,"cake-edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp=Cake.objects.get(id=id)
        form=CakeForm(instance=emp,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"changed successfully")
            return redirect("cake-detail",pk=id)
        messages.error(request,"not changed")
        return render(request,"cake-edit.html",{"form":form})
class CakeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Cake.objects.get(id=id).delete()
        messages.success(request,"cake deleted successfully")
        return redirect("cake-list")
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"registration.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"account has been created successfully")
            return redirect("signin")
        messages.error(request,"account not created")
        return render(request,"registration.html",{"form":form})
class SignInView(View):
    def get (self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login successfully")
                return redirect("cake-list")
        messages.error(request,"login error")
        return render(request,"login.html",{"form":form})
def signout(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

    

