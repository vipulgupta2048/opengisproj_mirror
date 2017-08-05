import logging
from .models import *
import json

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

def get_meta_fields(getjson=False):
    try:
        data = options.objects.filter(option_name="meta_field")
        jsonFields = []
        for d in data:
            temp = {}
            fields = json.loads(str(d.value))
            for x in fields:
                temp[x] = fields[x]
            temp["id"] = d.id
            temp["is_removable"] = d.is_removable
            jsonFields.append(temp)
        return jsonFields
    except Exception as e:
        toReturn = {}
        toReturn["status"] = "error"
        toReturn["msg"] = type(e) + e.message
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
            gis_meta = gis_data_meta.objects.filter(data=gis_id)    #Fetch all rows from gis_data_meta that contain data for gis_id 
            for y in gis_meta:
                obj[y.key] = y.value    #Add Every Key to dictionary with it's value
            arr.append(obj)    #Add Current Dictionary to arr
        return arr  #return the final arr
    except Exception as e:
        toReturn = {}
        toReturn["status"] = "error"
        toReturn["msg"] = type(e) + e.message
        toReturn["errcode"] = "500"
        return toReturn

def is_meta_key(key):
    try: 
        fields = get_meta_fields()
        flag = False
        for x in fields:
            if x['key_name'] == key:
                flag = True
                break
        return flag
    except Exception as e:
        toReturn = {}
        toReturn["status"] = "error"
        toReturn["msg"] = type(e) + e.message
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
            if(is_meta_key(key)):
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
            arr.append(obj)        
        return arr
    except Exception as e:
        return e

def add_param(data, user):
    toReturn = {}
    param = {}
    removable = False
    if(is_meta_key(data['key_name'])):
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
            jsonParam = json.dumps(param)
            p = options.objects.create(option_name="meta_field",value=jsonParam, is_removable = removable)
            p.save()
            toReturn["status"] = "success"
            toReturn["message"] = str(p.id)
        except Exception as e:
            toReturn["status"] = "error"
            toReturn["msg"] = type(e) + e.message
            toReturn["errcode"] = "500"

    return toReturn

def remove_param(option_id, user):
    try:
        obj = options.objects.filter(id=option_id)
        toReturn = {}
        if not obj:
            toReturn['status'] = "error"
            toReturn['msg'] = "Option Id Not Found"
            toReturn['errcode'] = "OPTION_DOES_NOT_EXIST"
        else:
            if(obj[0].is_removable):
                fields = json.loads(str(obj[0].value))
                keyName = fields['key_name']
                meta_rows = gis_data_meta.objects.filter(key=keyName)
                meta_rows.delete()
                obj.delete()  
                toReturn['status'] = "success"
            else:
                toReturn['status'] = "error"
                toReturn['msg'] = "Option Cannot be Removed"
                toReturn['errcode'] = "OPTION_IS_NOT_REMOVABLE"
    except Exception as e:
        toReturn["status"] = "error"
        toReturn["msg"] = type(e) + e.message
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
        toReturn["msg"] = type(e) + e.message
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
        toReturn["msg"] = type(e) + e.message
        toReturn["errcode"] = "500"

    return toReturn