from django.shortcuts import render
import json
from django.http import HttpResponse
# Create your views here.

def get_json_data():
    json_data = open("static/data.json", "r+")
    json_data = json.load(json_data)
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


def first_page(request):
    if request.method == "POST":
        data = request.POST.dict()
        value = data["userData"]
        json_data = get_json_data()
        json_data = sort_json_data(json_data, value)
        array = json_data["results"]
        return render(request, "showcard.html", {"arr": array})
    else:
        json_data = get_json_data()    
        array = json_data["results"]
        return render(request, "home.html", {"arr": array})


def put_data(request):
    select = request.GET.getlist('select',default=None)
    name = request.GET.getlist('name',default=None)
    price = request.GET.getlist('price',default=None)
    select = str(select[0])
    name = str(name[0])
    price = str(price[0])
    json_data = get_json_data()

    k = 0
    flag = False
    for val in json_data["results"]:
        if val["category"] == select:
            ob = {
                "title" : name,
                "price" : price
            }
            json_data["results"][k]["subjects"].append(ob)
            flag = True
        if flag:
            break
        k = k + 1

    myfile = open("static/data.json", "w")

    string = json.dumps(json_data)
    myfile.write(string)
    myfile.close() 
    
    return HttpResponse("Hello")