from django.shortcuts import render,redirect

from store.forms import SignUpForm

from django.views.generic import View



# Create your views here.

class SignUpview(View):

    template_name="register.html"

    form_class=SignUpForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":self.form_class})

    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            print("success")

            return redirect("register")

        else:

            print("failed")

            return render(request,self.template_name,{"form":form_instance})


