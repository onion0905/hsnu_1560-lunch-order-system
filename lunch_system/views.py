from django.http import HttpResponse
import json
import urllib.request as req
from django.shortcuts import render

def helloworld(request): 
    return HttpResponse('<b>Hello World! <i>您好</i></b>') 

def home(request):
    return HttpResponse('<b>歡迎來到我的首頁!</b>') 

def index(request):
    url = "https://shop.ichefpos.com/api/graphql/online_restaurant?op=restaurantMenuItemCategoriesQuery"
    requestdata = {"operationName":"restaurantMenuItemCategoriesQuery","variables":{"publicId":"aoU64iPV"},"query":"query restaurantMenuItemCategoriesQuery($publicId: String) {\n  restaurant(publicId: $publicId) {\n    menu {\n      categoriesSnapshot {\n        uuid\n        _id: uuid\n        name\n        menuItemSnapshot {\n          ...restaurantMenuItemBasicFields\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment restaurantMenuItemBasicFields on OnlineRestaurantMenuItemSnapshotOutput {\n  uuid\n  name\n  price\n  pictureFilename\n  menuItemType\n  description\n  isSoldOut\n  __typename\n}\n"}
    request_assembled = req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "Content-Type":"application/json",
        "op":"restaurantMenuItemCategoriesQuery"
    }, data = json.dumps(requestdata).encode("utf-8"))
    with req.urlopen(request_assembled) as response:
        result = response.read().decode("utf-8")

    result = json.loads(result)
    meals = result["data"]["restaurant"]["menu"]["categoriesSnapshot"][0]["menuItemSnapshot"]#['name']
    meal_list = []
    for meal in meals:
        element = meal['name'] + " " + str(int(meal['price']))
        meal_list.append(element)
    return render(request, 'index.html', locals())