from django.shortcuts import render,redirect
from .models import CustomUser, Book, Booking, Department
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.

def loginpage(request):
    return render(request, 'login.html')

def home(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        image = request.FILES.get('image')

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'Home/employer-register.html', {'message': "Username already exists"})
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'Home/employer-register.html', {'message': "Email already exists"})
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return render(request, 'Home/employer-register.html', {'message': "Phone number already exists"})

        data = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            email=email,
            pic=image,
            username=username,
            password=password,
            user_type="Student"
        )
        data.save()
        return redirect(Login)

    else:    
        return render(request, 'register.html')
    
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
         # Authenticate superusers (admins)
        admin_user = authenticate(request, username=username, password=password)
        if admin_user is not None and admin_user.is_staff:
            login(request, admin_user)
            return redirect(reverse('admin:index'))  # Redirect to the admin dashboard
        elif user is not None:
            # If not an admin, check regular users            
            login(request, user)
            if user.user_type == "Student":     #Student profile
                return redirect(student_home)
            elif user.user_type == "Teacher":   #Teacher profile
                return redirect(teacher_home)  
            elif user.user_type == "Librarian":   #Librarian profile
                return redirect(librarian_home)  
        else:
            context = {
                'message': "*Invalid credentials"
            }
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')
    
def Logout(request):
    logout(request)
    return redirect(Login)


###########################################################################################################
    
def teacher_home(request):
    return render(request, 'Teacher/user.html')

def view_students(request):
    return render(request, 'Teacher/students.html')










###########################################################################################################

def student_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    books = Book.objects.all()
    context = {
        'user':user,
        'books':books
    }
    return render(request, 'Student/index.html', context)

def student_books(request):
    return render(request, 'Student/books.html')

def view_book(request):
    return render(request, 'Student/view-book.html')

def student_profile(request):
    return render(request, 'Student/profile.html')

def student_history(request):
    return render(request, 'Student/user_history.html')

def nobook(request):
    return render(request, 'Student/nobook.html')


###############################################################################################################

def librarian_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'Librarian/user.html',{'user':user})

def view_books(request):
    books = Book.objects.all()
    return render(request, 'Librarian/books.html',{'books':books})

def edit_libprofile(request):
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.address = request.POST['address']
        user.phone_number = request.POST['phone_number']
        user.email = request.POST['email']
        user.username = request.POST['username']
        if 'image' in request.FILES:
            user.pic = request.FILES.get('image')
        user.save()
        return redirect(view_books)

def add_book(request):
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        bookname = request.POST['book_name']
        author = request.POST['author']
        genre = request.POST['genre']
        description = request.POST['description']
        image = request.FILES['image']
        data = Book.objects.create(librarian_id=user, bookname=bookname, author=author, genre=genre, description=description, image=image)
        data.save()
        return redirect(view_books)
    else: 
        return render(request, 'Librarian/add_book.html')

def edit_book(request,id):
    user = CustomUser.objects.get(id=request.user.id)
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        book.bookname = request.POST['book_name']
        book.author = request.POST['author']
        book.genre = request.POST['genre']
        book.description = request.POST['description']
        if 'image' in request.FILES:
            book.image = request.FILES['image']

        book.save()
        
        return redirect(view_books)
    else:
        context = {
            'id':id,
            'book':book
        }    
        return render(request, 'Librarian/edit-book.html', context)
    
def delete_book(request,id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect(view_books)