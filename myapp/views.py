from django.shortcuts import render
from decimal import Decimal
import pdfkit
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Bus, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import datetime
from . import validators

def home(request):
    # if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    # else:
        # return render(request, 'myapp/signin.html')

def contact(request):
    return render(request,'myapp/contact.html')

#@login_required(login_url='signin')
def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        bus_list = Bus.objects.filter(source=source_r, dest=dest_r, date=date_r)
        if bus_list:
            return render(request, 'myapp/list.html',{'bus_list':bus_list })
        else:
            context["error"] = "Sorry no buses availiable"
            return render(request, 'myapp/findbus.html', context)
    else:
        buses = Bus.objects.filter(date__gt= datetime.date.today())

        sources = []
        dests = []
        for bus in buses:
            sources.append(bus.source)
            dests.append(bus.dest)

        return render(request, 'myapp/findbus.html', {'sources':sources, 'dests':dests})


@login_required(login_url='signin')
def bookings(request, bus_id=1):
    context = {}
    if request.method == 'POST':
        id_r = bus_id
        seats_r = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=id_r)
        if bus:
            if bus.rem > int(seats_r):
                name_r = bus.bus_name
                cost = int(seats_r) * bus.price
                source_r = bus.source
                dest_r = bus.dest
                nos_r = Decimal(bus.nos)
                price_r = bus.price*seats_r
                date_r = bus.date
                time_r = bus.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = bus.rem - seats_r
                Bus.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, bus_name=name_r,
                                           source=source_r, busid=id_r,
                                           dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                # book.save()
                return render(request, 'myapp/bookings.html',{'book_id':book.id, 'book':book})
            else:
                context["error"] = "Sorry select fewer number of seats"
                return render(request, 'myapp/findbus.html', context,)

    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def cancellings(request, book_id=1):
    context = {}
    # if request.method == 'POST':
    if request.method == 'GET':

        id_r = book_id
        #seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            #nos_r = book.nos - seats_r
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'myapp/findbus.html', context)


# logout_required

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

def logout_required(function=None, logout_url=settings.LOGOUT_URL):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# logout_required end

@logout_required(logout_url='signout')
def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')

        context = {}

        if User.objects.filter(username=name_r).exists():
            context['error1']= 'Username already exists'
        if User.objects.filter(email=email_r).exists():
            context['error2']='Email already exists'
        
        if len(context) > 0:
            return render(request, 'myapp/signup.html', context)
        

        #validation of emaIL AND PASSWORD
        if(not validators.is_valid_email(email_r)):
            context['error1'] = 'Invalid Email'
        
        isPassValid, passValidMsg = validators.is_valid_password(password_r)
        if(not isPassValid):
            context['error2'] = passValidMsg
        
        if len(context) > 0:
            return render(request, 'myapp/signup.html', context)
        
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            return render(request, 'myapp/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/home.html', context)
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)

def ticket(request, id):
    context= Book.objects.get(pk=id)
    
    return render(request,'myapp/ticket.html',{'book':context})

def downloadPDF(request, id):
   pdfkit.from_url(f'http://127.0.0.1:8000/ticket/{id}/','ticket.pdf')
   with open('./ticket.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response