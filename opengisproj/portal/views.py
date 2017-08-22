from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import *
from .forms import UploadForm
# Create your views here.

def home(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/home')
    f = get_meta_fields()
    return render(request, 'portal/index.html', {'meta_fields': f})

def add(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/add')
    f = get_meta_fields()
    return render(request, 'portal/add-new.html', {'meta_fields': f})


def browse(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/browse')
    return render(request, 'portal/browse.html')


def addParam(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/parameters')
    return render(request, 'portal/add-param.html')


def dataGroups(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/datagroups')
    return render(request, 'portal/data-groups.html')


def reports(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/reports')
    return render(request, 'portal/reports.html')
def shapefilesManager(request):
    if request.user.is_authenticated == False:
        return redirect('/accounts/login?next=/portal/shapefiles')
    form = UploadForm()
    return render(request, 'portal/shapefiles.html',{'form':form, 'meta':'shapefile'})
def fileupload(request):
    if request.user.is_authenticated == False:
        return redirect('/accounts/login?next=/portal/shapefiles')
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'portal/upload.html', {'msg':"Successfully Uploaded!"})
    else:
        return HttpResponse(status=405)
def importView(request):
    if request.user.is_authenticated == False:
        return redirect('/account/login?next=/portal/importView')
    form = UploadForm()
    return render(request, 'portal/importView.html', {'form':form})
def processAjax(request, action):
    if request.user.is_authenticated == False:
        return JsonResponse("Unauthenticated Request", safe=False)
    if action == 'getmetafields':
        res = get_meta_fields()
        return JsonResponse(res, safe=False, content_type="text/html")
    elif action == "addNewData":
        if request.method == "POST":
            post_data = request.POST
            res = add_new_data(post_data, request.user, ret_json=True)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action == "getgisdata":
        if(request.method == "GET"):
            get_data = request.GET
            res = get_meta()
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action == "addnewparam":
        if(request.method == "POST"):
            post_data = request.POST
            res = add_param(post_data, user=request.user)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action == "removeparam":
        if(request.method == "POST"):
            post_data = request.POST
            res = remove_param(option_id=post_data['id'], group_id=post_data['data_group'], user=request.user)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action == "importgisdata":
        if(request.method == "POST"):
            post_data = request.POST
            res = import_gis_data(post_data['file_id'])
            return JsonResponse(res, safe=False, content_type="text/html")
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action == "getexceldatafrommapping":
        if(request.method == "POST"):
            post_data = request.POST
            res = get_excel_data_from_mapping(post_data['mapping'],post_data['file_id'], post_data['data_group'])
            return JsonResponse(res, safe=False, content_type="text/html")
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action == "removedata":
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
    elif action == "editparam":
        if(request.method == "POST"):
            post_data = request.POST
            res = edit_gis_param(param_key=post_data['key'],opt_id=post_data['paramId'],new_value=post_data['value'], user=request.user)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action == "getdatagroups":
        if(request.method == "GET"):
            get_data = request.GET
            res = get_data_groups()
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action == "addnewdatagroup":
        if(request.method == "POST"):
            post_data = request.POST
            res = add_data_group(post_data, request.user)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action == "removedatagroup":
        if(request.method == "POST"):
            post_data = request.POST
            res = remove_data_group(group_id = post_data['group_id'], user=request.user)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action == "editdatagroup":
        if(request.method == "POST"):
            post_data = request.POST
            res = edit_data_group(group_id = post_data['group_id'], key = post_data['key'], new_value = post_data['value'], user=request.user)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action=="getshapefilecoord":
        if(request.method == "GET"):
            get_data = request.GET
            res = shapefile_reader(get_data['shapeId'])
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action=="getuploadedshapefiles":
        if(request.method == "GET"):
            res = getuploadedshapefiles()
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action=="addnewshape":
        if(request.method == "POST"):
            post_data = request.POST
            res = create_new_shape(post_data)
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action=="getshapes":
        if(request.method == "GET"):
            res = get_shapes()
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    elif action=="getexcelfiles":
        if(request.method == "GET"):
            res = get_excel_files()
            return JsonResponse(res, safe=False)
        else:
            return JsonResponse("Form Data Missing or Invalid Request", safe=False)
    else:
        return JsonResponse("Invalid Action", safe=False)