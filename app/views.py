from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout as LG
from app.models import *
from django.contrib import messages
from requests import Session
from bs4 import BeautifulSoup as bs
import requests
import json
import re
import pandas as pd
import psycopg2
import mysql.connector as sqltor
from django.contrib.auth.decorators import login_required
from django.conf import settings

databases = settings.DATABASES

default_db = databases['default']

mycon = psycopg2.connect(user=rootdefault_db['USER'],password=default_db['PASSWORD'],database=default_db['NAME'],host=default_db['HOST'])
# mycon = psycopg2.connect(user="root",password="root",database="scrapper_db",host="localhost")
mycur = mycon.cursor()
s = Session()
s.headers["User-Agent"] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'
proxy = {"https":"http://scraperapi:029bb147a727d6d82383e3704952d291@proxy-server.scraperapi.com:8001"}

def logout(request):
    LG(request)
    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def home(request):
    c = addproduct.objects.filter(user_id=request.user.id)
    return render(request,"index.html",{"user":request.user,"product":c})

def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            client_key = request.POST['g-recaptcha-response']
            print(client_key)
            secret_key = "6LdqctUZAAAAAHScMialGIw3eDfO4-GqrECXZaGX"
            captchadata = {
                'secret':secret_key,
                'response':client_key
            }
            r = requests.post("https://www.google.com/recaptcha/api/siteverify",data=captchadata)
            response = json.loads(r.text)
            print(response)
            verify  = response["success"]
            print(verify)
            if verify is not True:
                return render(request,"login.html")
            else:
                return HttpResponseRedirect("/")
        else:
            # messages.error(request,'username or password not correct')
            return render(request,'login.html',{"error":True})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            return render(request,'login.html',{"error":False})

def Export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format("export_csv")
    df = pd.DataFrame(temp.objects.all().values_list("sku","link","web_price","our_price","offers","express","sot","time"),columns=["SKU","Link","Web Price","our price","offers","express","sot","time"])
    df.to_csv(response)
    return response


def register(request):
    if request.method=="POST":
        d = dict(request.POST)
        print(d)
        u = User.objects.create(username=d["name"][0],email=d["gmail"][0])
        u.set_password(d['password'][0])
        u.save()
        return HttpResponseRedirect("/login")
    else:
        return render(request,'signup.html')


@login_required(login_url="/login/")
def add_product(request):
    if(request.method=="POST"):
        r = dict(request.POST)
        # objects = [i for i in Category.objects.all()]

        # oc = [str(i) for i in objects]
        cat = request.POST.get("Category")
        # g_cat= r["Category"][0]
        # idd = oc.index(g_cat)+1
        # cat = Category.objects.get(id=id)
        a = addproduct.objects.create(user_id = request.user.id,sku=r['sku'][0],Product_link=r['prod_link'][0],min_price =r['min_price'][0],our_category_id=cat,Freezed=r["Freeze"][0])
        a.save()
        print(r)
    return render(request,'add_prod.html',{"Categories":Category.objects.all()})
@login_required(login_url="/login/")
def add_cat(request):

    if(request.method=="POST"):
        r1 = dict(request.POST)
        a1 = Category.objects.create(Category_name =r1["Category Name"][0])
        a1.save()
        print(r1)
    return render(request,'add_cat.html')
@login_required(login_url="/login/")

def product(request):
    return render(request,'products.html')


def detail(request,id):
    prd = addproduct.objects.get(id=id)
    # category = Category.ob
    return render(request,"detail.html",{"product":prd,"edit":False})

def delete(request,id):
    remove = addproduct.objects.get(id=id)
    remove.delete()
    return HttpResponseRedirect("/")


def Edit(request,id):
    if request.method == 'GET':
        prd = addproduct.objects.get(id=id)
        cat = Category.objects.all()
        return render(request,"detail.html",{"product":prd,"edit":True,"category":cat})
    else:
        product = addproduct.objects.get(id=id)
        category = request.POST.get('category')
        prod_link = request.POST.get('link')
        price = request.POST.get('price')
        freeze = request.POST.get('freeze')

        product.Product_link = prod_link
        product.our_category_id = category
        product.Freezed = freeze
        product.min_price = price
        product.save()


        return HttpResponseRedirect("/product/detail/{}/".format(id))

def scraped(request):
    # if(request.method=="GET"):
    query1 = "delete from app_temp"
    mycur.execute(query1)
    mycon.commit()
    query =  'select * from app_addproduct where user_id ={};'.format(request.user.id)
    mycur.execute(query)
    data = mycur.fetchall()

    for i in range(0,len(data)):
        r =  s.get(data[i][1],proxies=proxy,verify=False)
        soup = bs(r.content,'html.parser')
        sku = re.search('https://www.noon.com/uae-en/(.*?)/(.*?)/p?',data[i][1]).group(2)
        Price = soup.find('span','sellingPrice').text
        if(soup.find("span","cta")):
            Sot = soup.find("div","soldBy").text
            Offers = soup.find("div","panelContainer").find("h3").text[:2]
            if(soup.find("div","shippingEstimatorContainer").find("img","fbn")):
                express = "Yes"
            else:
                express= "No"
        else:
            if(soup.find("div","shippingEstimatorContainer").find("img","fbn")):
                express = "Yes"
            else:
                express= "No"
            Sot=soup.find("p","sellerName").find("a").text
            Offers = "NaN"
        aa =temp.objects.create(sku=sku,link=data[i][1],web_price=Price,our_price=data[i][2],offers=Offers,express=express,sot=Sot)
        aa.save()
        print("**********************************************")
    return render(request,'data.html',{'data':temp.objects.all()})

@login_required(login_url="/login/")
def crawler(request):
    return render(request,'crawler.html')
