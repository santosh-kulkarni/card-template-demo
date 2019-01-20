from django.shortcuts import render
import json

# Create your views here.


def get_json_data():
    json_data = open("static/data.json")
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
