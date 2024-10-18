from django.shortcuts import render,redirect

from django.urls import reverse_lazy

from store.forms import SignUpForm,SignInform

from django.contrib.auth import authenticate,login,logout

from django.views.generic import View,FormView,CreateView,TemplateView



# Create your views here.

class SignUpview(CreateView):

    template_name="register.html"

    form_class=SignUpForm

    success_url=reverse_lazy("login")

    

class SigninView(FormView):

    template_name="login.html"

    form_class=SignInform

    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")

            pwd=form_instance.cleaned_data.get("password")

            user_obj=authenticate(username=uname,password=pwd)

            if user_obj:

                login(request,user_obj)

                return redirect("index")

        return render(request,self.template_name,{"form":form_instance})        


class Indexview(TemplateView):

    template_name="index.html"
