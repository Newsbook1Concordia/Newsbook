
from django.shortcuts import render
import requests
API_KEY = '90237a5a846744c38ba89566f26af087'

# Create your views here.
def login(request):
    return render(request,'login.html',{})

def news(request):
   
    url = f'https://newsapi.org/v2/top-headlines?country=ca&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    if request.method == 'POST' :
        check = request.POST.getlist('category')
    context = {
        'articles' : articles,
        'category' : check,
        
    }
    
    return render(request,'news.html',context)

def category(request):
    return render(request,'category.html',{})

def country(request):
    return render (request,"countrycode-container")


    