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
    path('', views.loginpage, name="loginpage"),
    path('home', views.home, name="home"),
    path('register', views.register, name="register"),
    path('Login', views.Login, name="Login"),
    path('Logout',views.Logout, name="Logout"),


    path('teacher_home', views.teacher_home, name="teacher_home"),
    path('edit_teacherprofile', views.edit_teacherprofile, name="edit_teacherprofile"),
    path('view_students', views.view_students, name="view_students"),
    path('search_student', views.search_student, name="search_student"),
    path('student_records/<int:id>', views.student_records, name="student_records"),
    path('view_departments', views.view_departments, name="view_departments"),
    path('view_teachers/<int:id>', views.view_teachers, name="view_teachers"),

    path('student_home', views.student_home, name="student_home"),
    path('view_teacher', views.view_teacher, name="view_teacher"),
    path('departments', views.departments, name="departments"),
    path('student_books', views.student_books, name="student_books"),
    path('std_booksearch', views.std_booksearch, name="std_booksearch"),
    path('view_book/<int:id>', views.view_book, name="view_book"),
    path('booking', views.booking, name="booking"),
    path('student_profile', views.student_profile, name="student_profile"),
    path('edit_stdprofile', views.edit_stdprofile, name="edit_stdprofile"),
    path('student_history', views.student_history, name="student_history"),
    path('return_book/<int:id>', views.return_book, name="return_book"),
    path('nobook',views.nobook, name="nobook"),

    path('librarian_home', views.librarian_home, name="librarian_home"),
    path('view_books', views.view_books, name="view_books"),
    path('search_book', views.search_book, name="search_book"),
    path('edit_libprofile', views.edit_libprofile, name="edit_libprofile"),
    path('add_book', views.add_book, name="add_book"),
    path('edit_book/<int:id>', views.edit_book, name="edit_book"),
    path('delete_book/<int:id>', views.delete_book, name="delete_book"),
    path('librarian_history', views.librarian_history, name="librarian_history"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)