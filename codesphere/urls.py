"""codesphere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from store import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpview.as_view(),name="register"),
    path('login/',views.SigninView.as_view(),name="login"),
    path('index/',views.Indexview.as_view(),name="index"),
    path('logout/',views.logout_view.as_view(),name="logout"),
    path('profile/edit',views.ProfileEditView.as_view(),name="profile-edit"),
    path('project/add',views.ProjectCreateView.as_view(),name='project-create'),
    path('mywork/all',views.MyprojectListView.as_view(),name="my-work"),
    path('project/<int:pk>/change',views.ProjectUpdateView.as_view(),name='project-change'),
    path('project/<int:pk>/detail',views.ProjectDetailView.as_view(),name='project-detail'),
    path('project/<int:pk>/wishlist',views.AddWishListItemView.as_view(),name='wishlist'),
    path('mywishlist',views.MyListWishListView.as_view(),name='mywish'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
