from django.shortcuts import render,redirect
from .models import CustomUser, Book, Booking, Department
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        department = request.POST['department']
        print(department)
        username = request.POST['username']
        password = request.POST['password']
        image = request.FILES.get('image')

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'Home/employer-register.html', {'message': "Username already exists"})
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'Home/employer-register.html', {'message': "Email already exists"})
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return render(request, 'Home/employer-register.html', {'message': "Phone number already exists"})
        department_data = Department.objects.get(department_name=department)
        print(department_data)
        data = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            email=email,
            pic=image,
            department_id=department_data,
            username=username,
            password=password,
            user_type="Student"
        )
        data.save()
        return redirect(Login)

    else:
        departments = Department.objects.all()    
        return render(request, 'register.html',{'departments':departments})
    
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


##############################################        TEACHER       ######################################################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)    
def teacher_home(request):
    return render(request, 'Teacher/user.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def edit_teacherprofile(request):
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
        return redirect(teacher_home)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def view_students(request):
    user = CustomUser.objects.get(id=request.user.id)
    students = CustomUser.objects.filter(department_id=user.department_id, user_type='Student')
    context = {
        'user': user,
        'students': students
    }
    return render(request, 'Teacher/students.html', context)


def search_student(request):
    User = CustomUser.objects.get(id=request.user.id)
    if request.method == 'GET':
        search_query = request.GET.get('search')
        if search_query:
            students = CustomUser.objects.filter(department_id=User.department_id, user_type='Student', username__icontains=search_query)
            context = {
                'user': User,
                'students': students
            }
            return render(request, 'Teacher/students.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def student_records(request,id):
    user = CustomUser.objects.get(id=id)
    bookings = Booking.objects.filter(username=user)
    print(bookings)
    context = {
        'bookings': bookings
    }
    return render(request,'Teacher/studentbookings.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)  
def view_departments(request):
    departments = Department.objects.all()
    context = {
        'departments':departments
    }
    return render(request, 'Teacher/departments.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)  
def view_teachers(request,id):
    department = Department.objects.get(id=id)
    teachers = CustomUser.objects.filter(department_id=department, user_type='Teacher')
    context = {
        'teachers': teachers
    }
    return render(request, 'Teacher/teachers.html', context)







#############################################         STUDENT            ####################################################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def student_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    books = Book.objects.all()
    context = {
        'user':user,
        'books':books
    }
    return render(request, 'Student/index.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def view_teacher(request):
    user = CustomUser.objects.get(id=request.user.id)
    teachers = CustomUser.objects.filter(user_type="Teacher")
    context = {
        'user':user,
        'teachers':teachers
    }
    return render(request, 'Student/teachers.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def departments(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'Student/departments.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def student_books(request):
    user = CustomUser.objects.get(id=request.user.id)
    books = Book.objects.all()
    context = {
        'user':user,
        'books':books
    }
    return render(request, 'Student/books.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def view_book(request,id):
    user = CustomUser.objects.get(id=request.user.id)
    book = Book.objects.get(id=id)
    context = {
        'user':user,
        'book':book
    }
    return render(request, 'Student/view-book.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def std_booksearch(request):
    User = CustomUser.objects.get(id=request.user.id)
    if request.method == 'GET':
        search_query = request.GET.get('search')
        if search_query:
            books = Book.objects.filter(bookname__icontains=search_query)
            return render(request, 'Student/books.html', {'books':books})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def booking(request):
    user = CustomUser.objects.get(id=request.user.id)
    if request.method=='POST':
        bookid=request.POST["bookid"]
        currentbook=Book.objects.get(id=bookid)
        if Booking.objects.filter(bookname=currentbook, status="booked").exists():
            return redirect(nobook)
        else:
            data=Booking.objects.create(username=user, bookname=currentbook, status="booked")
            data.save()
            return render(request,'Student/bookingsuccess.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def student_profile(request):
    return render(request, 'Student/profile.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def edit_stdprofile(request):
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
        return redirect(student_home)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def student_history(request):
    user = CustomUser.objects.get(id=request.user.id)
    data = Booking.objects.filter(username=user).order_by('status')
    context={
        'user':user,
        'data':data
    }
    return render(request, 'Student/user_history.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def return_book(request,id):
    user = CustomUser.objects.get(id=request.user.id)
    booking = Booking.objects.get(id=id)

    booking.returndate = timezone.now()
    booking.status = "returned"
    booking.save()
    return redirect(student_history)

def nobook(request):
    return render(request, 'Student/nobook.html')


####################################################      LIBRARIAN     ###########################################################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def librarian_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'Librarian/user.html',{'user':user})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def view_books(request):
    books = Book.objects.all()
    items_per_page = 10
    # Use Paginator to paginate the products
    paginator = Paginator(books, items_per_page)
    page = request.GET.get('page', 1)
    try:
        bookdata = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        bookdata = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        bookdata = paginator.page(paginator.num_pages)
    return render(request, 'Librarian/books.html',{'books':bookdata})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def search_book(request):
    User = CustomUser.objects.get(id=request.user.id)
    if request.method == 'GET':
        search_query = request.GET.get('search')
        if search_query:
            books = Book.objects.filter(bookname__icontains=search_query)
            return render(request, 'Librarian/books.html', {'books':books})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
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
        return redirect(librarian_home)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)       
def delete_book(request,id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect(view_books)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=Login)   
def librarian_history(request):
    user = CustomUser.objects.get(id=request.user.id)
    bookings = Booking.objects.all().order_by('returndate')
    current_date = timezone.now().date()
    items_per_page = 10
    # Use Paginator to paginate the products
    paginator = Paginator(bookings, items_per_page)
    page = request.GET.get('page', 1)
    try:
        bookdata = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        bookdata = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        bookdata = paginator.page(paginator.num_pages)
    context = {
        'bookings':bookdata,
        'current_date':current_date
    }
    return render(request, 'Librarian/history.html', context)