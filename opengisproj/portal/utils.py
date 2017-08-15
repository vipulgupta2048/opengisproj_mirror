import logging
import os
from .models import *
import json
import numpy as np
import pandas as pd
import decimal
from decimal import *

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
    try:
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
    except Exception as e:
        toReturn = {}
        toReturn["status"] = "error"
        toReturn["msg"] = type(e) + e.message
        toReturn["errcode"] = "500"
        return toReturn

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

def test():
    arr = get_meta_fields(True)
    print(arr)

def import_gis_data():
    Location = os.getcwd() + '/portal/data1.xlsx'
    df = pd.read_excel(Location, 0, index_col='Sl. No')
    excelFields = df.columns
    temp = []
    for x in excelFields:
        temp.append(x)
    print(temp)
    return temp

def get_excel_data_from_mapping(mapping):
    mappingString = mapping['mapping']
    mappingObjects = json.loads(mappingString)
    metaFields = get_meta_fields()

    def get_meta_attributes(meta_key):
        for x in metaFields:
            obj = x
            if obj['key_name'] == meta_key:
                attr = {}
                for x in obj:
                    attr[x] = obj[x]
                return attr
        return False #"{max:value, min:value, required:'true'}"

    excelData = {}
    approved = []
    rejected = []
    Location = os.getcwd() + '/portal/data1.xlsx'
    df = pd.read_excel(Location, 0, index_col='Sl. No')
 #   accepted = pd.DataFrame(columns = columns)
    for row in df.itertuples():
        print("Iterating new row!")
        print(row)
        obj = {}
        flag = 0
     #   attr = get_meta_attributes(mappingObjects['db_key'])
        for x in mappingObjects:
            db_key = x['db_key']    #select current db key from array
            excel_key = x['excel_key']
            df.rename(columns={excel_key : db_key}, inplace=True)
            attr = get_meta_attributes(db_key) #Get it's attributes array of db_key
            #print(attr)
            excel_header = db_key #Value of 
            excel_val = df.ix[row.Index][db_key]
  #          print(x['excel_key'])
  #          excel_value = r'row.' + excel_key
   #         obj['excel_value'] = excel_value #"value from x['excel-key']"
            # print(x['db_key']+":"+x['excel_key'])
            if attr['key_name'] == db_key:
                print("Key:"+attr['key_name']+" type:"+attr['key_type']+" max: "+attr['max'])
                obj[attr['key_name']] = excel_val #attr['step']
                if attr['key_type'] == 'number':
                    step = decimal.Decimal(float(attr['step']))
                    step.as_tuple().exponent
                    print(step)
                    
                    round(excel_val, step)
                    if float(excel_val) < float(attr['min']) or float(excel_val) > float(attr['max']):
                        print("flag is 1")
                        flag = 1
                elif attr['key_type'] == 'text' and attr['max_len'] != '':
                    if str(len(excel_val)) > int(attr['max_len']):
                        flag = 1
        print("ROw created")
        print(obj)
        if flag == 1:
            print("REJECTED")
            rejected.append(obj)
        else:
            print("APPROVED")
            approved.append(obj)
      #      accepted = pd.DataFrame()
    excelData["approved"] = approved
    excelData["rejected"] = rejected
    print("excelData")
    print(excelData)
    eD = pd.DataFrame(excelData)
    return excelData
#   array = [{db_key:'lorem', excel_key:'ipsum'},{db_key:'', excel_key:''},{db_key:'', excel_key:''},{db_key:'', excel_key:''}]
#   array = []
#   loop: (row wise)  
#       obj = {}
#       obj[lorem]  = excelKeyvalue ((excel file's ipsum column)) of row x
#       obj[dbkey2] = value
#       array.append(obj)
#   loopend
#   array = ["aaproved":[{
#       dbkey1: value,
#       dbkey2:value },{}],"rejected": [{},{}]
# ]
#
#
#
#    arr = get_meta_fields(True)
#    print(arr)
#    excelFields.dtype.names = 


