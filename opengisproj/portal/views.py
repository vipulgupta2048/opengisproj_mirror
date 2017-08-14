from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import *
# Create your views here.

def demo(request):
    install(user=request.user)
    return HttpResponse("OK")

def home(request):
    if request.user.is_authenticated == True:
        f = get_meta_fields()
        return render(request, 'portal/index.html', {'meta_fields':f})
    else:
        return redirect('/account/login?next=/portal/home')

def add(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/add')
    f = get_meta_fields()
    return render(request, 'portal/add-new.html', {'meta_fields':f})

def browse(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/browse')
    return render(request, 'portal/browse.html')
def addParam(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/parameters')
    return render(request, 'portal/add-param.html')
def reports(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/reports')
    return render(request, 'portal/reports.html')
def importView(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/importView')
    return render(request, 'portal/importView.html')
#def importView(request):
 #   test()
   # return JsonResponse("Success", safe=False)
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
    elif action=="importgisdata":
        if(request.method == "POST"):
            post_data = request.POST
            res = import_gis_data()
            return JsonResponse(res, safe=False, content_type="text/html")
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action=="getexceldatafrommapping":
        if(request.method == "POST"):
            post_data = request.POST
            res = get_excel_data_from_mapping(post_data)
            return JsonResponse(res, safe=False, content_type="text/html")
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action=="removedata":
        if(request.method == "POST"):
            post_data = request.POST
            res = remove_gis_data(data_id=post_data['id'], user=request.user)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action == "editdata" :
        if(request.method == "POST"):
            post_data = request.POST
            res = edit_gis_data(meta_key=post_data['key'],data_id=post_data['dataId'],new_value=post_data['value'], user=request.user)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    else:
        return JsonResponse("Invalid Action", safe=False)