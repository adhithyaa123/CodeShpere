from django.shortcuts import render,redirect,get_object_or_404

from django.urls import reverse_lazy

from store.forms import SignUpForm,SignInform,UserprofileForm,ProjectForm,PasswordResetForm

from django.contrib.auth import authenticate,login,logout

from store.models import Project,WishListItem,Order

from django.views.generic import View,FormView,CreateView,TemplateView

from django.contrib import messages

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

from django.db.models import Sum

from django.core.mail import send_mail

from store.decorators import signin_required

from django.views.decorators.cache import never_cache

from decouple import config
# Create your views here.

def send_email():

    send_mail(
    "codehub project download",
    "You have completed purchase of project.",
    "uadhithya23@gmail.com",
    ["adhithyau2003@gmail.com"],
    fail_silently=False,
)

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


decs=[signin_required,never_cache]
@method_decorator(decs,name="dispatch")
class Indexview(TemplateView):

    template_name="index.html"

    def get(self,request,*args,**kwargs):

        qs=Project.objects.all().exclude(developer=request.user)

        return render(request,self.template_name,{"data":qs})


    
@method_decorator(decs,name="dispatch")
class logout_view(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("login")

@method_decorator(decs,name="dispatch")
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


@method_decorator(decs,name="dispatch")
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


@method_decorator(decs,name="dispatch")
class MyprojectListView(View):

    template_name="my_project_list.html"

    def get(self,request,*args,**kwargs):

        qs=Project.objects.filter(developer=request.user)

        return render(request,self.template_name,{"data":qs})


@method_decorator(decs,name="dispatch")
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


@method_decorator(decs,name="dispatch")
class ProjectDetailView(View):

    template_name="project_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Project.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})

@method_decorator(decs,name="dispatch")
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
        

@method_decorator(decs,name="dispatch")
class MyListWishListView(View):

    template_name="mywishlist.html"

    def get(self,request,*args,**kwargs):

            qs=request.user.basket.basket_item.filter(is_order_placed=False)    

            total=qs.values("project_object").aggregate(total=Sum("project_object__price")).get("total")

            print("totalllll",total)        

            return render(request,self.template_name,{"data":qs,"total":total})

@method_decorator(decs,name="dispatch")
class WishListItemDelete(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        WishListItem.objects.get(id=id).delete()

        return redirect("mywish")


import razorpay
@method_decorator(decs,name="dispatch")
class CheckOutView(View):

    template_name="checkout.html"

    def get(self,request,*args,**kwargs):

        # step1 razorpay authentication

        KEY_ID=config("KEY_ID")

        KEY_SECRET=config("KEY_SECRET")

        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        wish_list_total=request.user.basket.basket_item.filter(is_order_placed=False).values("project_object").aggregate(total=Sum("project_object__price")).get("total")

        data={  "amount":wish_list_total*100, "currency":"INR", "receipt":"order_receipt_11"  }

        payment=client.order.create(data=data)

        order_id=payment.get("id")

        order_obj=Order.objects.create(order_id=order_id,customer=request.user)

        wishlist_item=request.user.basket.basket_item.filter(is_order_placed=False)

        for wi in wishlist_item:

            order_obj.wishlist_item_objects.add(wi)

            wi.is_order_placed=True

            wi.save()    

                 

        return render(request,self.template_name,{"key_id":KEY_ID,"amount":wish_list_total,"order_id":order_id})

@method_decorator(csrf_exempt,name='dispatch')
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)

        KEY_ID=config("KEY_ID")

        KEY_SECRET=config("KEY_SECRET")

        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        try:

            client.utility.verify_payment_signature(request.POST)

            order_id=request.POST.get("razorpay_order_id")
            
            obj=Order.objects.filter(order_id=order_id).update(is_paid=True)

            send_email()

            print("success")

        except:

            print("failed")

        return redirect("myorder")


@method_decorator(decs,name="dispatch")
class MyOrderView(View):

    template_name="myorders.html"

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(customer=request.user)

        return render(request,self.template_name,{"data":qs})

from django.contrib.auth.models import User

class PasswordResetView(View):



    template_name="password_reset.html"

    form_class=PasswordResetForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            username=form_instance.cleaned_data.get("username")

            email=form_instance.cleaned_data.get("email")

            password1=form_instance.cleaned_data.get("password1")

            password2=form_instance.cleaned_data.get("password2")

            print(username,email,password1,password2)

            try:

                assert password1==password2,"Password Mismatch"

                user_object=User.objects.get(username=username,email=email)

                user_object.set_password(password2)

                user_object.save()

                return redirect("login")

            except Exception as e:

                messages.error(request,f"{e}")

        return render(request,self.template_name,{"form":form_instance})



