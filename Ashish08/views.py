import os
from django.db import models
import uuid
import requests
import allauth
import requests
from allauth.account.models import EmailAddress
from Lib.db import User
from django.shortcuts import render

from google.oauth2 import id_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import google.auth.transport.requests

API_KEY = '90237a5a846744c38ba89566f26af087'


from sqlalchemy import Column, Integer,String,ForeignKey,INTEGER,Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy.orm import sessionmaker
import uuid

import os
from sqlalchemy import create_engine, MetaData,Table,Column,String,ForeignKey,INTEGER,Float
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()

#   User Table


# Create your views here.
os.environ["DATABASE_URL"] = "cockroachdb://ashish:O6dEEC2SpIwwfc03nwsOZQ@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dlair-python-2718"
engine = create_engine(os.environ["DATABASE_URL"])


Session=sessionmaker(bind=engine)
session=Session()

def update_country(session,email,country):
    req=session.query(User).filter(User.Email == email).first()
    req.Country=country
class User(Base):
    
    __tablename__ = 'User'
    id = Column(UUID(as_uuid=True), primary_key = True)
    Email = Column(String)
    Name = Column(String)
    Country = Column(String)
    
    # category=relationship("Category")



########## Add User To Table
def add_user(name,email,country):
    user_id = uuid.uuid4()
    new_user = User(id=user_id,Email=email,Name=name,Country=country)
    session.add(new_user)
    
############ Get User Information From User Email
def get_user_info(email):
    user:User=session.query(User).filter(User.Email == email).first()
    return user


def login(request):
  
    
    return render(request,'login.html',{})

def news(request):
    
    if request.method == 'POST' :
        print(".......................")
        country = request.POST.get('country')
        
        
        
    url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    if request.method == 'POST' :   
        check = request.POST.getlist('category')
        print(check)
    
    context = {
        'articles' : articles,
        'category' : check,
        'country'  : country,
        
    }

    return render(request,'news.html',context)



def category(request):
    # name = get.EmailAddress
    
    name=request.user
    name_user = str(name)
    print('............')
    print(name_user)
    
    email=request.user.email
    
    # add_user(name_user,email,country)
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

# def country(request):

    
#     return render (request,"countrycode-container")

    
def profile(request):
    return render(request,'profile.html',{})

def business(request):  
    email=User.Email
    cat= get_user_info(User.Email)
    
    print(cat)
    print('..........country............')
    country=User.Country
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


 
    