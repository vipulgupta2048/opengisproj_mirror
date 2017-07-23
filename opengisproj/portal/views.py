from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import *
# Create your views here.

def demo(request):
    install(user=request.user)
    return HttpResponse("OK")

def home(request):
    if request.user.is_authenticated():
        f = get_meta_fields()
        return render(request, 'index.html', {'meta_fields':f})
    else:
        return redirect('/admin/')

def add(request):
    if request.user.is_authenticated == False:
        return redirect('/admin/')
    f = get_meta_fields()
    return render(request, 'add-new.html', {'meta_fields':f})

def browse(request):
    if request.user.is_authenticated == False:
        return redirect('/admin/')
    return render(request, 'browse.html')
def addParam(request):
    if request.user.is_authenticated == False:
        return redirect('/admin/')
    return render(request, 'add-param.html')

def processAjax(request, action):
    if request.user.is_authenticated == False:
        return JsonResponse("Unauthenticated Request", safe=False)
    if action=='getmetafields':
        res = get_meta_fields(True)
        return JsonResponse(res, safe=False, content_type="text/html")
    elif action=="addNewData":
        if request.method == "POST":
            post_data = request.POST
            res = str(add_new_data(post_data, request.user))
            toReturn = {}
            toReturn["status"] = "success"
            toReturn["id"] = res
            return JsonResponse(toReturn, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action=="getgisdata":
        if(request.method == "GET"):
            get_data = request.GET
            res = get_meta()
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action=="addnewparam":
        if(request.method == "POST"):
            post_data = request.POST
            res = add_param(post_data, user=request.user)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action=="removeparam":
        if(request.method == "POST"):
            post_data = request.POST
            res = remove_param(option_id=post_data['id'], user=request.user)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    else:
        return JsonResponse("Invalid Action", safe=False)