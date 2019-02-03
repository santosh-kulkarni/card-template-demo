from django.shortcuts import render
import json
import urllib
import requests
import pyrebase
from django.http import HttpResponse
config = {
    'apiKey': "AIzaSyDFCngrd6jrP1o6vvi63rdMZHX7kZyUvqI",
    "authDomain": "my-card-app.firebaseapp.com",
    "databaseURL": "https://my-card-app.firebaseio.com",
    "projectId": "my-card-app",
    "storageBucket": "my-card-app.appspot.com",
    "messagingSenderId": "590654162532"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def get_json_data():
    data = db.child("results").get()
    json_data = {
        "results": []
    }
    for result in data.each():
        json_data["results"].append(result.val())
    return json_data


def sort_json_data(json_data, value):
    i = 0
    j = 0
    for val in json_data["results"]:  
        j = 0
        count = 0

        for sub in val["subjects"]:
            if value.lower() not in sub["title"].lower():
                json_data["results"][i]["subjects"][j] = None
                count = count + 1
            j = j + 1

        if count == len(val["subjects"]):
            json_data["results"][i]["presence"] = None

        i = i + 1
    return json_data


def get_subject_count(array):
    answer = 0
    for val in array:
        count = 0
        if val["presence"]:
            for sub in val["subjects"]:
                if sub is not None:
                    count = count + 1
        answer = answer + count
    return answer


def load_category(array):
    category = []
    for val in array:
        category.append(val["category"])
    return category


def first_page(request):
    if request.method == "POST":
        data = request.POST.dict()
        value = data["userData"]
        json_data = get_json_data()
        json_data = sort_json_data(json_data, value)
        array = json_data["results"]
        sub_count = get_subject_count(array)
        return render(request, "showcard.html", {"arr": array, "total": sub_count})
    else:
        json_data = get_json_data()    
        array = json_data["results"]
        sub_count = get_subject_count(array)
        category = load_category(array)
        return render(request, "home.html", {"arr": array, "total": sub_count, "category": category})


def get_children_count(select):
    data = db.child("results").get()
    count = 0
    flag = True
    current = 0
    for result in data.each():
        if result.val()["category"] == select:
            flag = False
            for val in result.val()["subjects"]:
                count = count + 1

        if flag:
            current = current + 1
        else:
            break
    
    send_data = {
        "current": current,
        "count": count
    }
    return send_data


def put_data(request):
    select = request.GET.getlist('select',default=None)
    name = request.GET.getlist('name',default=None)
    price = request.GET.getlist('price',default=None)
    select = str(select[0])
    name = str(name[0])
    price = str(price[0])
    new_data = {
        "title": name,
        "price": price
    }
    num = get_children_count(select)
    db.child("results").child(num["current"]).child("subjects").child(num["count"]).set(new_data)
    return HttpResponse("Hello")