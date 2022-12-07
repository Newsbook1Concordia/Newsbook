import json
import os
from django.db import models
import uuid
from django.http import HttpResponse
import requests
import allauth
import requests
# from Lib.db import User
from django.shortcuts import render
# from google.oauth2 import id_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import google.auth.transport.requests
from sqlalchemy import Column, Integer,String,ForeignKey,INTEGER,Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy.orm import sessionmaker
import uuid
import os
from sqlalchemy import create_engine, MetaData,Table,Column,String,ForeignKey,INTEGER,Float
from sqlalchemy.dialects.postgresql import UUID
from projects.models import FriendRequest, FriendList
API_KEY ='90237a5a846744c38ba89566f26af087'
Base = declarative_base()

# Create your views here.
os.environ["DATABASE_URL"] = "cockroachdb://ashish:ltb1Pj_BqF4Yp0exVkfuWA@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dlair-python-2718"
engine = create_engine(os.environ["DATABASE_URL"])
Session=sessionmaker(bind=engine)
session=Session()


class User(Base):
    __tablename__ = 'User'
    id = Column(UUID(as_uuid=True), primary_key = True)
    Email = Column(String)
    Name = Column(String)
    Country = Column(String)
    
    category=relationship("Category")
class Category(Base):
    __tablename__="Category"
    id = Column(UUID(as_uuid=True), primary_key = True)
    user_id=Column(UUID(as_uuid=True),ForeignKey("User.id"))
    category=Column(String)
    
    
def addUser(email,name,country):
    user_id = uuid.uuid4()
    new_user=User(id=user_id, Email=email,Name=name,Country=country)
    session.add(new_user)
    return user_id
    
def update_country(session,email,country):
    req=session.query(User).filter(User.Email == email).first()
    req.Country=country
    
def get_user_info(email):                                                   ############ Get User Information From User Email
    user:User=session.query(User).filter(User.Email == email).first()
    return user


##########################################################################################

def remove_friend(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			try:
				removee = Account.objects.get(pk=user_id)
				friend_list = FriendList.objects.get(user=user)
				friend_list.unfriend(removee)
				payload['response'] = "Successfully removed that friend."
			except Exception as e:
				payload['response'] = f"Something went wrong: {str(e)}"
		else:
			payload['response'] = "There was an error. Unable to remove that friend."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to remove a friend."
	return HttpResponse(json.dumps(payload), content_type="application/json")
######################################################################################################################

def addCategory(session,category):
    
    cat_id = uuid.uuid4()
    new_category=User(id=cat_id,Category=category)
    session.add(new_category)
    return cat_id


def login(request):
  return render(request,'login.html',{})

def news(request):
    email=request.user.email
    
    




  
    if request.method == 'POST' :
        print("............country...........")
        country = request.POST.get('country')
        print(country)
        update_country(session,email,country)
        cat= get_user_info(User.Email)
        print('.................Business.............')
     # email=request.user.email
        print(cat)
        print('..........country............')
        # country2=cat.Country
        # print(country2)
        print('.........country updated in database')
    url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
    response = requests.get(url)
    
    data = response.json()
    articles = data['articles']
    if request.method == 'POST' :   
        check = request.POST.getlist('category')
        # check = 'sports'
        # addCategory(session,check)
        
        print(check)
    context = {
        'articles' : articles,
        'category' : check,
        'country'  : country,
        # 'response' : data1,
    }
    return render(request,'news.html',context)

def category(request):                      ######After login Category selection
    # name = get.EmailAddress
    
    ema=request.user.email
    email=str(ema)
    username=str(request.user)
    default ='ca'
    # print(default)
    addUser(email,username,default)
    print('newprint')
    print('............')
    print(username)
    print(email)
    print('...........get user......')
    a= (get_user_info(email))
    print(a.Country)
    # add_user(name,email)
    # email='kartik.faldu1207@gmail.com'
    # user = get_user_info(email)
    
    # # print(uid)
    # print(user.Country)
    # u=User(first_name='waqas',email='my@yahoo.com')
    # u.save()
    # print(user.Name)
    print('-----------------0---------')
    # print(email)
    # add_user(name,email,category)
    return render(request,'category.html',{})

def search(request): 
    

    check=request.GET.get('search')
    print(check)
    url2 = f'https://newsapi.org/v2/everything?q={check}&from=2022-11-18&sortBy=popularity&apiKey={API_KEY}'
    response = requests.get(url2)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles,
        
        }
    return render(request,'search.html',context)  

# def country(request):

    
#     return render (request,"countrycode-container")  
def profile(request):                ####### User Profile
    return render(request,'profile.html',{})

def business(request): #########1st Category wise
    
    cat= get_user_info(User.Email)
    print('.................Business.............')
     # email=request.user.email
    print(cat)
    print('..........country............')
    country=cat.Country
    print(country)
    # if request.method == 'POST' :
    #     country = request.POST.get('country')
    url2 = f'https://newsapi.org/v2/top-headlines?country={country}&category=business&apiKey={API_KEY}'
    response = requests.get(url2)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles,
        # 'category' : check,
        'country'  : country,
        
     }
    return render(request,'business.html',context)   

def general(request): #########1st Category wise
    
    cat= get_user_info(User.Email)
    print('.................Business.............')
     # email=request.user.email
    print(cat)
    print('..........country............')
    country=cat.Country
    print(country)
    # if request.method == 'POST' :
    #     country = request.POST.get('country')
    url2 = f'https://newsapi.org/v2/top-headlines?country={country}&category=general&apiKey={API_KEY}'
    response = requests.get(url2)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles,
        # 'category' : check,
        'country'  : country,
        
     }
    return render(request,'general.html',context)   

def sports(request):                        #########2nd Category wise
    
    cat= get_user_info(User.Email)
    print('.................SPorts.............')                                   # email=request.user.email
    print(cat)
    print('..........country............')
    country=cat.Country
    print(country)
    # if request.method == 'POST' :
    #     country = request.POST.get('country')
    url3 = f'https://newsapi.org/v2/top-headlines?country={country}&category=sports&apiKey={API_KEY}'
    response = requests.get(url3)
    data = response.json()
    articles2 = data['articles']
    context = {
        'articles' : articles2,
        # 'category' : check,
        'country'  : country,
        
     }
    return render(request,'sports.html',context)   


def science(request): #########1st Category wise
    
    cat= get_user_info(User.Email)
    print('.................Science.............')
     # email=request.user.email
    print(cat)
    print('..........country............')
    country=cat.Country
    print(country)
    # if request.method == 'POST' :
    #     country = request.POST.get('country')
    url2 = f'https://newsapi.org/v2/top-headlines?country={country}&category=science&apiKey={API_KEY}'
    response = requests.get(url2)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles,
        # 'category' : check,
        'country'  : country,
        
     }
    return render(request,'science.html',context)   

def entertainment(request): #########1st Category wise
    
    cat= get_user_info(User.Email)
    print('.................Science.............')
     # email=request.user.email
    print(cat)
    print('..........country............')
    country=cat.Country
    print(country)
    # if request.method == 'POST' :
    #     country = request.POST.get('country')
    url2 = f'https://newsapi.org/v2/top-headlines?country={country}&category=entertainment&apiKey={API_KEY}'
    response = requests.get(url2)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles,
        # 'category' : check,
        'country'  : country,
        
     }
    return render(request,'entertainment.html',context)   

def technology(request): #########1st Category wise
    
    cat= get_user_info(User.Email)
    print('.................Science.............')
     # email=request.user.email
    print(cat)
    print('..........country............')
    country=cat.Country
    print(country)
    # if request.method == 'POST' :
    #     country = request.POST.get('country')
    url2 = f'https://newsapi.org/v2/top-headlines?country={country}&category=technology&apiKey={API_KEY}'
    response = requests.get(url2)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles,
        # 'category' : check,
        'country'  : country,
        
     }
    return render(request,'technology.html',context)   



 
    

 
    