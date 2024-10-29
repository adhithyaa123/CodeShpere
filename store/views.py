from django.shortcuts import render,redirect,get_object_or_404

from django.urls import reverse_lazy

from store.forms import SignUpForm,SignInform,UserprofileForm,ProjectForm

from django.contrib.auth import authenticate,login,logout

from store.models import Project

from django.views.generic import View,FormView,CreateView,TemplateView

from django.contrib import messages



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

    def get(self,request,*args,**kwargs):

        qs=Project.objects.all().exclude(developer=request.user)

        return render(request,self.template_name,{"data":qs})


    

class logout_view(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("login")

class ProfileEditView(View):

    template_name="profile_edit.html"

    form_class=UserprofileForm

    def get(self,request,*args,**kwargs):

        profile_user_instance=request.user.profile

        form_instance=UserprofileForm(instance=profile_user_instance)

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        profile_user_instance=request.user.profile

        form_instance=UserprofileForm(request.POST,instance=profile_user_instance,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("index")

        

        return render(request,self.template_name,{"form":form_instance})


class ProjectCreateView(View):

    template_name="project_create.html"

    form_class=ProjectForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})


    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST,files=request.FILES)

        if form_instance.is_valid():

            form_instance.instance.developer=request.user

            form_instance.save()

            return redirect("index")

        return redirect(request,self.template_name,{"form":form_class})    



class MyprojectListView(View):

    template_name="my_project_list.html"

    def get(self,request,*args,**kwargs):

        qs=Project.objects.filter(developer=request.user)

        return render(request,self.template_name,{"data":qs})

class ProjectUpdateView(View):

    template_name="project_update.html"

    form_class=ProjectForm

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_obj=Project.objects.get(id=id)

        form_instance=self.form_class(instance=project_obj)

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_obj=Project.objects.get(id=id)

        form_instance=self.form_class(request.POST,instance=project_obj,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("my-work")

        return render(request,self.template_name,{"form":form_instance})


class ProjectDetailView(View):

    template_name="project_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Project.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})


class AddWishListItemView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_object=get_object_or_404(Project,id=id)

        try:

            request.user.basket.basket_item.create(project_object=project_object)

            print("wish list item added")

            messages.success(request,"added success to wishlist")

        except Exception as e:

            messages.error(request,"failed")
    

        return redirect("index")
        


class MyListWishListView(View):

    template_name="mywishlist.html"

    def get(self,request,*args,**kwargs):

            qs=request.user.basket.basket_item.filter(is_order_placed=False)            

            return render(request,self.template_name,{"data":qs})

