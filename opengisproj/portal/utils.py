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

def get_meta():
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

def is_meta_key(key):
    fields = get_meta_fields()
    flag = False
    for x in fields:
        if x['key_name'] == key:
            flag = True
            break
    return flag

def add_new_data(post_data, request_user, ret_json=False):
    is_first = True
    gis_id = -1
    for x in post_data:
        key = x
        val = post_data[key]
        if(is_meta_key(key)):
            if(is_first):
                g = gis_data.objects.create(created_by=request_user)
                g.save()
                gis_id = g
                is_first=False
            m = gis_data_meta.objects.create(key=key, value=val, data=gis_id)
            m.save()
    if(ret_json):
        return {"id":str(gis_id.id)}
    else:
        return gis_id.id

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
        jsonParam = json.dumps(param)
        p = options.objects.create(option_name="meta_field",value=jsonParam, is_removable = removable)
        p.save()
        toReturn["status"] = "success"
        toReturn["message"] = str(p.id)
    return toReturn

def remove_param(option_id, user):
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
    return toReturn