from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, Transaction
from django.utils import timezone
from decimal import Decimal
import csv
from django.db.models import Sum
from django.http import JsonResponse
from django.views.generic import TemplateView
import plotly.express as px
from plotly.offline import plot
from plotly.graph_objs import Scatter

import logging 
l = logging.getLogger('django.db.backends') 
l.setLevel(logging.DEBUG) 
l.addHandler(logging.StreamHandler())


def home(request):
    return render(request, 'homepage.html')

def signupUser(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if len(username)<5:
            messages.error(request, "Length is too small")
            return redirect('signup.html')
        
        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, "You account has been successfully created! You can now login!")
        return redirect('login') 

    return render(request, 'signup.html')      

def loginUser(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful! You are welcome!")
            return render(request, 'userhome.html', {'user':request.user})
        else:
            messages.error(request, "Invalid credentials! Please try again!") 
            return redirect('login')

    return render(request, 'login.html')          

@login_required
def editprofile(request):
    
    if request.method == "POST":

        if request.POST['username']:
            request.user.username= request.POST.get('username')
        if request.POST['firstname']:
            request.user.first_name = request.POST.get('firstname')
        if request.POST['lastname']:
            request.user.last_name = request.POST.get('lastname')       

        request.user.save()

        messages.success(request, "Profile updated successfully!  Please login again!")
        return redirect('login')
    
    return render(request, 'editprofile.html', {'user':request.user})

@login_required
def logoutUser(request):
    logout(request)
    messages.success(request, "User logged out successfully!") 
    return redirect('homepage')    

@login_required
def userhome(request):
    return render(request, 'userhome.html')

@login_required
def usertransactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'usertransactions.html', locals())

@login_required
def addtransaction(request):
    if request.method == "POST":
        transaction = Transaction(value=request.POST.get("value"), memo=request.POST.get("memo"))
        category_name = request.POST.get("category")
        existing_category = Category.objects.filter(name=category_name).first()
        transaction.category = existing_category
        transaction.date=request.POST.get("date")
        transaction.user=request.user
        transaction.save()

        messages.success(request, "Transaction added successfully!")
        return redirect('usertransactions')

    category = Category.objects.all()
    return render(request, 'addtransaction.html',{'category':category})

@login_required
def exporttransaction(request):
     
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Category', 'Value', 'Description', 'Date'])

    for transaction in Transaction.objects.select_related('category').filter(user=request.user).values_list('category__name','value', 'memo', 'date'):
        writer.writerow(transaction)

    response['Content-Disposition']='attachment;filename="expenses.csv"'    

    return response
    
@login_required
def analysis(request):
    
    #Day wise expense
    x1_data=[]
    y1_data=[]

    transactions = Transaction.objects.filter(user=request.user).order_by('date')

    for transaction in transactions:
        x1_data.append(transaction.date)
        y1_data.append(transaction.value)
    
    fig = px.bar(x=x1_data, y=y1_data,labels={'x':"Day",'y':'Expense'})
    daywise = fig.to_html(full_html=False)

    #Food wise expense
    x1_data=[]
    y1_data=[]

    transactions = Transaction.objects.filter(user=request.user,category=(Category.objects.filter(name='Food').first())).order_by('date')
  
    for transaction in transactions:
        x1_data.append(transaction.date)
        y1_data.append(transaction.value)

    fig = px.bar(x=x1_data, y=y1_data, labels={'x':"Day",'y':'Expense'})
    foodwise = fig.to_html(full_html=False)

    #Rent wise expense
    x1_data=[]
    y1_data=[]

    transactions = Transaction.objects.filter(user=request.user,category=(Category.objects.filter(name='Rent').first())).order_by('date')
  
    for transaction in transactions:
        x1_data.append(transaction.date)
        y1_data.append(transaction.value)

    fig = px.bar(x=x1_data, y=y1_data, labels={'x':"Day",'y':'Expense'})
    rentwise = fig.to_html(full_html=False)

    #Electricity wise expense
    x1_data=[]
    y1_data=[]

    transactions = Transaction.objects.filter(user=request.user,category=(Category.objects.filter(name='Electricity').first())).order_by('date')
  
    for transaction in transactions:
        x1_data.append(transaction.date)
        y1_data.append(transaction.value)

    fig = px.bar(x=x1_data, y=y1_data, labels={'x':"Day",'y':'Expense'})
    elecwise = fig.to_html(full_html=False)

    #Maintainence wise expense
    x1_data=[]
    y1_data=[]

    transactions = Transaction.objects.filter(user=request.user,category=(Category.objects.filter(name='Maintainence').first())).order_by('date')
  
    for transaction in transactions:
        x1_data.append(transaction.date)
        y1_data.append(transaction.value)

    fig = px.bar(x=x1_data, y=y1_data, labels={'x':"Day",'y':'Expense'})
    maintainwise = fig.to_html(full_html=False)

    #Entertainment wise expense
    x1_data=[]
    y1_data=[]

    transactions = Transaction.objects.filter(user=request.user,category=(Category.objects.filter(name='Entertainment').first())).order_by('date')
  
    for transaction in transactions:
        x1_data.append(transaction.date)
        y1_data.append(transaction.value)

    fig = px.line(x=x1_data, y=y1_data, labels={'x':"Day",'y':'Expense'})
    entertainwise = fig.to_html(full_html=False)

    #Recharge wise expense
    x1_data=[]
    y1_data=[]

    transactions = Transaction.objects.filter(user=request.user,category=(Category.objects.filter(name='Recharge').first())).order_by('date')
  
    for transaction in transactions:
        x1_data.append(transaction.date)
        y1_data.append(transaction.value)

    fig = px.bar(x=x1_data, y=y1_data, labels={'x':"Day",'y':'Expense'})
    rechargewise = fig.to_html(full_html=False)

    #Education wise expense
    x1_data=[]
    y1_data=[]

    transactions = Transaction.objects.filter(user=request.user,category=(Category.objects.filter(name='Education').first())).order_by('date')
  
    for transaction in transactions:
        x1_data.append(transaction.date)
        y1_data.append(transaction.value)

    fig = px.bar(x=x1_data, y=y1_data, labels={'x':"Day",'y':'Expense'})
    eduwise = fig.to_html(full_html=False)

    return render(request, 'analysis.html', {'daywise':daywise,'foodwise':foodwise,
                                             'rentwise':rentwise,'elecwise':elecwise,
                                             'maintainwise':maintainwise, 'entertainwise':entertainwise,
                                             'rechargewise':rechargewise,'eduwise':eduwise})

