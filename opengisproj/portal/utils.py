import logging
import os
from .models import *
import json
import shapefile
import os
from django.conf import settings
import numpy as np
import pandas as pd

def install(user):
    temp = options.objects.create(option_name="meta_field",value='{"key_name": "bod", "label": "BOD", "key_type": "number", "min": "", "max": "", "max_len": "", "step": "0.000001", "required": "True"}')
    temp.save()
    temp = options.objects.create(option_name="meta_field",value='{"key_name": "ph", "label": "ph Value", "key_type": "number", "min": "", "max": "", "max_len": "", "step": "0.00001", "required": "True"}')
    temp.save()
    temp = options.objects.create(option_name="meta_field",value='{"key_name": "longitude", "label": "Longitude", "key_type": "number", "min": "-180", "max": "180", "max_len": "", "step": "0.000001", "required": "True"}', is_removable=False)
    temp.save()
    temp = options.objects.create(option_name="meta_field",value='{"key_name": "latitude", "label": "Latitude", "key_type": "number", "min": "-90", "max": "90", "max_len": "", "step": "0.000001", "required": "True"}', is_removable=False)
    temp.save()
    temp = options.objects.create(option_name="meta_field",value='{"key_name": "year", "label": "Year", "key_type": "number", "min": "1947", "max": "2100", "max_len": "", "step": ""}', is_removable=False)
    temp.save()

def get_meta_fields(filterByGroup=None):
    try:
        if(filterByGroup == None):
            data = options.objects.filter(option_name="meta_field")
        else:
            filterByGroup = int(filterByGroup)
            group = data_groups.objects.filter(id=filterByGroup)
            data = options.objects.filter(option_name="meta_field", data_group=group)
        jsonFields = []
        for d in data:
            temp = {}
            fields = json.loads(str(d.value))
            for x in fields:
                temp[x] = fields[x]
            temp["id"] = str(d.id)
            temp["is_removable"] = d.is_removable
            temp["data_group"] = str(d.data_group.id)
            jsonFields.append(temp)
        return jsonFields
    except Exception as e:
        toReturn = {}
        toReturn["status"] = "error"
        toReturn["msg"] = e
        toReturn["errcode"] = "500"
        return toReturn

def get_meta():
    try:
        gis_objects = gis_data.objects.all()    #Fetch all rows from gis_data
        arr = []    #Create a new array to return
        for x in gis_objects:
            obj = {}    #Create new empty dictionary
            gis_id = x.id
            obj["id"] = str(gis_id)  #Add Id to dictionary
            obj["data_group"] = str(x.data_group.id)
            gis_meta = gis_data_meta.objects.filter(data=gis_id)    #Fetch all rows from gis_data_meta that contain data for gis_id 
            for y in gis_meta:
                obj[y.key] = y.value    #Add Every Key to dictionary with it's value
            arr.append(obj)    #Add Current Dictionary to arr
        return arr  #return the final arr
    except Exception as e:
        toReturn = {}
        toReturn["status"] = "error"
        toReturn["msg"] = e
        toReturn["errcode"] = "500"
        return toReturn

def is_meta_key(key, data_group):
    try: 
        fields = get_meta_fields()
        flag = False
        for x in fields:
            print(x['data_group'])
            if x['key_name'] == key and str(x['data_group']) == data_group :
                flag = True
                break
        return flag
    except Exception as e:
        toReturn = {}
        toReturn["status"] = "error"
        toReturn["msg"] = e
        toReturn["errcode"] = "500"

    return toReturn

def add_new_data(post_data, request_user, ret_json=False):
    toReturn = {}
    try:
        is_first = True
        gis_id = -1
        group_id = data_groups.objects.filter(id=post_data["data_group"])
        if not group_id:
            return False
        group_id = group_id[0]
        for x in post_data:
            key = x
            val = post_data[key]
            if(is_meta_key(key, post_data["data_group"])):
                if(is_first):
                    g = gis_data.objects.create(created_by=request_user, data_group = group_id)
                    g.save()
                    gis_id = g
                    is_first=False
                m = gis_data_meta.objects.create(key=key, value=val, data=gis_id)
                m.save()
        if(ret_json):
            toReturn["status"] = "success"
            toReturn["id"] = gis_id.id
        else:
            return gis_id.id
    except Exception as e:
        toReturn["status"] = "error"
        print(e)
        toReturn["msg"] = e
        toReturn["errcode"] = "500"

    return toReturn

def get_data_groups(): 
    try:
        groups = data_groups.objects.all()
        arr = []
        for x in groups:
            obj = {}
            obj['id'] = x.id
            obj['name'] = x.name
            obj['is_removable'] = x.is_removable
            arr.append(obj)        
        return arr
    except Exception as e:
        return e

def add_param(data, user):
    toReturn = {}
    param = {}
    removable = False
    if(is_meta_key(data['key_name'],data['data_group'])):
        toReturn["status"] = "error"
        toReturn["message"] = "Key Already Exists"
        toReturn["errcode"] = "KEY_EXISTS"
    else:
        for x in data:
            key = x
            val = data[x]
            if x=="csrfmiddlewaretoken":
                continue
            if x=="required":
                val="True"
            if x=="is_removable":
                removable = True
                continue
            param[key] = val
        try:
            group_id = data_groups.objects.filter(id=data["data_group"])[0]
            jsonParam = json.dumps(param)
            p = options.objects.create(option_name="meta_field",value=jsonParam, is_removable = removable, data_group = group_id)
            p.save()
            toReturn["status"] = "success"
            toReturn["message"] = str(p.id)
        except Exception as e:
            toReturn["status"] = "error"
            toReturn["msg"] = "Some error"
            toReturn["errcode"] = "500"

    return toReturn

def remove_param(option_id, group_id, user):
    try:
        obj = options.objects.filter(id=option_id, data_group = group_id)
        toReturn = {}
        if not obj:
            toReturn['status'] = "error"
            toReturn['msg'] = "Option Id Not Found"
            toReturn['errcode'] = "OPTION_DOES_NOT_EXIST"
        else:
            if(obj[0].is_removable):
                fields = json.loads(str(obj[0].value))
                keyName = fields['key_name']
                gis_data_objects = gis_data.objects.filter(data_group = group_id)
                for gis_obj in gis_data_objects:
                    meta_rows = gis_data_meta.objects.filter(key=keyName, data=gis_obj)
                    meta_rows.delete()
                obj.delete()  
                toReturn['status'] = "success"
            else:
                toReturn['status'] = "error"
                toReturn['msg'] = "Option Cannot be Removed"
                toReturn['errcode'] = "OPTION_IS_NOT_REMOVABLE"
    except Exception as e:
        toReturn["status"] = "error"
        toReturn["msg"] = e
        toReturn["errcode"] = "500"

    return toReturn

def remove_gis_data(data_id, user):
    try:
        obj = gis_data.objects.filter(id=data_id)
        toReturn = {}
        if not obj:
            toReturn['status'] = "error"
            toReturn['msg'] = "Data Id Not Found"
            toReturn['errcode'] = "DATA_DOES_NOT_EXIST"
        else:
            obj_meta = gis_data_meta.objects.filter(data_id=data_id)
            obj_meta.delete()
            obj.delete()
            temp = gis_data.objects.filter(id=data_id)
            if not temp:
                toReturn['status'] = "success"
            else:
                toReturn['status'] = "error"
                toReturn['msg'] = "Internal Error"
                toReturn['errcode'] = "INTERNAL_ERROR"
    except Exception as e:
        toReturn["status"] = "error"
        toReturn["msg"] = e
        toReturn["errcode"] = "500"

    return toReturn

def edit_gis_data(meta_key, data_id, new_value, user):
    try:
        obj = gis_data_meta.objects.get(key=meta_key, data=data_id)
        toReturn = {}
        if not obj:
            toReturn['status'] = "error"
            toReturn['msg'] = "Data Id Not Found"
            toReturn['errcode'] = "DATA_DOES_NOT_EXIST"
        else:
            obj.value = new_value
            obj.save()
            toReturn['status'] = "success"
    except Exception as e:
        toReturn["status"] = "error"
        toReturn["msg"] = e
        toReturn["errcode"] = "500"
        return toReturn

def edit_gis_param(param_key, opt_id, new_value, user):
    toReturn = {}
    try:
        obj = options.objects.filter(id=opt_id)[0]
        jsonFields = []
        flag = False
        if param_key == 'is_removable':
            if new_value == "True":
                obj.is_removable = True
            else:
                obj.is_removable = False
            flag = True
        else:
            fields = json.loads(obj.value)
            for attr in fields:
                if(attr == param_key):
                    fields[attr] = new_value
                    flag = True
                    break
            if flag == False:
                fields[param_key] = new_value
            obj.value = json.dumps(fields)
        obj.save()
        toReturn['status'] = 'success'
    except Exception as e:
        toReturn["status"] = "error"
        toReturn["msg"] = e
        toReturn["errcode"] = "500"
    return toReturn

def add_data_group(data, user):
    toReturn = {}
    try:
        removable = False
        if 'is_removable' in data:
            removable = True
        group = data_groups.objects.create(name=data['group_name'],is_removable=removable)
        group.save()
        toReturn['status'] = "success"
        toReturn['message'] = group.id
    except Exception as e:
        toReturn["status"] = "error"
        toReturn["msg"] = e
        toReturn["errcode"] = "500"
    return toReturn

def remove_data_group(group_id, user):
    toReturn = {}
    try:
        obj = data_groups.objects.filter(id=group_id)
        toReturn = {}
        if not obj:
            toReturn['status'] = "error"
            toReturn['msg'] = "Group Id Not Found"
            toReturn['errcode'] = "GROUP_DOES_NOT_EXIST"
        else:
            obj = obj[0]
            if obj.is_removable == False:
                toReturn['status'] = "error"
                toReturn['msg'] = "Group Cannot be Deleted"
                toReturn['errcode'] = "GROUP_NOT_REMOVABLE"
            else:
                obj_data = gis_data.objects.filter(data_group=obj)
                for x in obj_data:
                    obj_meta = gis_data_meta.objects.filter(data=x)
                    obj_meta.delete()
                obj_data.delete()
                obj.delete()
                toReturn['status'] = "success"
    except Exception as e:
        toReturn["status"] = "error"
        toReturn["msg"] = e
        toReturn["errcode"] = "500"
    return toReturn

def edit_data_group(group_id, key, new_value, user):
    toReturn = {}
    try:
        obj = data_groups.objects.filter(id=group_id)[0]
        if key == "name":
            obj.name = new_value
        elif key == "is_removable":
            if(new_value == "False"):
                obj.is_removable = False
            else:
                obj.is_removable = True
        obj.save()
        toReturn["status"] = "success"
    except Exception as e:
        toReturn["status"] = "error"
        toReturn["msg"] = e
        toReturn["errcode"] = "500"
    return toReturn

def shapefile_reader(shape_id):
    try:
        shapeDb = shapefiles.objects.filter(id=int(shape_id))[0]
        MEDIA_ROOT = settings.MEDIA_ROOT.replace('\\','/')+'/'
        shpFile = open(MEDIA_ROOT+str(shapeDb.shp_file.file_ref), "rb")
        dbfFile = open(MEDIA_ROOT+str(shapeDb.dbf_file.file_ref), "rb")
        shxFile = open(MEDIA_ROOT+str(shapeDb.shx_file.file_ref),"rb")
        sf = shapefile.Reader(shp=shpFile, dbf=dbfFile)
        shapes = sf.shapes()
        data = []
        for x in range(len(shapes)):
            curr_shape = sf.shape(x)
            pairs = []
            for point in range(len(curr_shape.points)):
                pairs.append({"lat":curr_shape.points[point][1], "lng":curr_shape.points[point][0]})
            data.append(pairs)
        return data
    except Exception as e:
        return str(e)

def getuploadedshapefiles():
    try:
        shapefiles = uploads.objects.filter(file_meta="shapefile")
        arr = []
        for x in shapefiles:
            obj = {}
            obj['id'] = x.id
            obj['file_name'] = x.file_name
            obj['description'] = x.description
            obj['file_path'] = str(x.file_ref)
            arr.append(obj)
        return arr
    except Exception as e:
        return "Error"

def create_new_shape(data):
    toReturn = {}
    try:
        shp_file_id = int(data['shp_file_id'])
        shx_file_id = int(data['shx_file_id'])
        dbf_file_id = int(data['dbf_file_id'])
        shpFile = uploads.objects.filter(id=shp_file_id)[0]
        dbfFile = uploads.objects.filter(id=dbf_file_id)[0]
        shxFile = uploads.objects.filter(id=shx_file_id)[0]
        shape_name = data['shape_name']
        shape = shapefiles.objects.create(shape_name=shape_name, shp_file = shpFile, shx_file = shxFile, dbf_file = dbfFile)
        toReturn['status'] = "success"
        toReturn['msg'] = shape.id
    except Exception as e:
        toReturn['status'] = "error"
        toReturn['msg'] = str(e)
    return toReturn

def get_shapes():
    try:
        shapes = shapefiles.objects.all()
        data = []
        for shape in shapes:
            obj = {}
            obj['shape_name'] = shape.shape_name
            obj['id'] = shape.id
            data.append(obj)
        return data
    except Exception as e:
        return str(e)

def import_gis_data(file_id):
    file_id = int(file_id)
    file_path = uploads.objects.filter(id=file_id)[0]
    MEDIA_ROOT = settings.MEDIA_ROOT.replace('\\','/')+'/'
    Location = MEDIA_ROOT+str(file_path.file_ref)
    df = pd.read_excel(Location, 0, index_col='Sl. No')
    excelFields = df.columns
    temp = []
    for x in excelFields:
        temp.append(x)
    return temp

def get_excel_data_from_mapping(mapping, file_id, data_group):
    mappingString = mapping
    mappingObjects = json.loads(mappingString)
    metaFields = get_meta_fields(data_group)

    def get_meta_attributes(meta_key):
        for x in metaFields:
            obj = x
            if obj['key_name'] == meta_key:
                attr = {}
                for x in obj:
                    attr[x] = obj[x]
                return attr
        return False
    excelData = {}
    approved = []
    rejected = []
    file_path = uploads.objects.filter(id=file_id)[0]
    MEDIA_ROOT = settings.MEDIA_ROOT.replace('\\','/')+'/'
    Location = MEDIA_ROOT+str(file_path.file_ref)
    df = pd.read_excel(Location, 0, index_col='Sl. No')
    for row in df.itertuples():
        obj = {}
        flag = 0
        for x in mappingObjects:
            db_key = x['db_key']    #select current db key from array
            excel_key = x['excel_key']
            df.rename(columns={excel_key : db_key}, inplace=True)
            attr = get_meta_attributes(db_key) #Get it's attributes array of db_key
            excel_header = db_key
            excel_val = df.ix[row.Index][db_key]
            if attr['key_name'] == db_key:
                print("Key:"+attr['key_name']+" type:"+attr['key_type']+" max: "+attr['max'])
                obj[attr['key_name']] = str(excel_val)
                if attr['key_type'] == 'number':
                    if attr['step']!= '':
                        step = float(attr['step'])
                        prec = int(len(str(step))- len(str(np.floor(step)))+1)
                        excel_val = round(excel_val,prec)
                    if excel_val != '' and attr['min']!='' and attr['max']!='':
                        if float(excel_val) < float(attr['min']) or float(excel_val) > float(attr['max']):
                            flag = 1
                elif attr['key_type'] == 'text' and attr['max_len'] != '':
                    if str(len(excel_val)) > int(attr['max_len']):
                        flag = 1
        if flag == 1:
            rejected.append(obj)
        else:
            approved.append(obj)
    excelData["approved"] = approved
    excelData["rejected"] = rejected
    return excelData

def get_excel_files():
    sheets = uploads.objects.filter(file_meta="excel_file")
    data = []
    for sheet in sheets:
        obj = {}
        obj['id'] = sheet.id
        obj['file_name'] = sheet.file_name
        obj['file_path'] = str(sheet.file_ref)
        data.append(obj)
    return data