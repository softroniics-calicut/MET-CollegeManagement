"""
URL configuration for College_Management_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginpage),
    path('home', views.home, name="home"),
    path('register', views.register, name="register"),
    path('Login', views.Login, name="Login"),
    path('Logout',views.Logout, name="Logout"),


    path('teacher_home', views.teacher_home, name="teacher_home"),
    path('view_students', views.view_students, name="view_students"),

    path('student_home', views.student_home, name="student_home"),
    path('student_books', views.student_books, name="student_books"),
    path('view_book', views.view_book, name="view_book"),
    path('student_profile', views.student_profile, name="student_profile"),
    path('student_history', views.student_history, name="student_history"),
    path('nobook',views.nobook, name="nobook"),

    path('librarian_home', views.librarian_home, name="librarian_home"),
    path('view_books', views.view_books, name="view_books"),
    path('edit_libprofile', views.edit_libprofile, name="edit_libprofile"),
    path('add_book', views.add_book, name="add_book"),
    path('edit_book/<int:id>', views.edit_book, name="edit_book"),
    path('delete_book/<int:id>', views.delete_book, name="delete_book"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)