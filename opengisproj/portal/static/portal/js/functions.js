var apiURI = '/portal/ajax/';

function getMetaFields(callbackFunc){
    gis_meta_fields_stored = false;
    $.ajax({
        url: apiURI+'getmetafields',
        type: "GET",
        dataType: "JSON",
        success: function(response){
            r = response;
            callbackFunc(r);
        },
        error: function(response){
            console.log("Error");
            console.log(response);
        }
    });
}

function storeMetaFields(data){
    gisMetaFields = data;
    gis_meta_fields_stored = true;
}

function importgisdata(callbackFunc){
    $.ajax({
        url: apiURI+'importgisdata',
        type: "POST",
        data: "csrfmiddlewaretoken="+csrftoken,
        dataType: "JSON",
        success: function(response){
            r = response;
            callbackFunc(r);
        },
        error: function(response){
            console.log("Error");
            console.log(response);
        }
    });
}

function getExcelDataFromMapping(mapping, callbackFunc){
    var mappingString = JSON.stringify(mapping);
    $.ajax({
        url: apiURI+'getexceldatafrommapping',
        type: 'POST',
        data: 'csrfmiddlewaretoken='+csrftoken+"&mapping="+mappingString,
        dataType: "JSON",
        success: function(response){
            r = response;
            callbackFunc(r);
        },
        error: function(response){
            console.log("Error");
            console.log(response);
        }
    });
}
function submitImporterData(data){
    console.log("Submitting data...");
}
function getGisData(callbackFunc){
    $.ajax({
        url: apiURI+'getgisdata',
        type: "GET",
        dataType: "JSON",
        success: function(response){
            r = response;
            callbackFunc(r);
        },
        error: function(response){
            console.log("Error");
            console.log(response);
        }
    });
}

function storeGisData(data){
    gisData = data;
    gis_data_stored = true;
}

function getGisGroups(callbackFunc){
    $.ajax({
        url: apiURI+'getdatagroups',
        type: "GET",
        dataType: "JSON",
        success: function(response){
            r = response;
            callbackFunc(r);
        },
        error: function(response){
            console.log("Error");
            console.log(response);
        }
    });
}

function storeGisGroups(data){
    gisGroups = data;
    gis_groups_stored = true;
}

function loadDataGroupSelector(element){
    $.each(element, function(index,value){
        var $this = $(this);
        var timer = setInterval(function(){
            if(gis_groups_stored == true){
                clearInterval(timer);
                $.each(gisGroups, function(i,v){
                    $this.append('<option value="'+v.id+'">'+v.name+' (id:'+v.id+' )</option>');
                });
            }
            $this.attr("data-groups-loaded","true");
        }, 200);
    });
}

function addMetaFieldAttributes(key_name){
    /** Accept Key Name and return a string containing HTML <input> attributes */
    var field_attr = '';
    $.each(gisMetaFields, function(i,v){
        if(v.key_name == key_name){
            field_attr+=' type="'+v.key_type+'"';
            // Check for min attribute
            if(v.min!="Null" && v.min!="undefined" && v.min!=undefined)
                field_attr+=' min="'+v.min+'"';
            // Check for Max Attribute
            if(v.max!="Null" && v.max!="undefined" && v.max!=undefined)
                field_attr+=' max="'+v.max+'"';
            // Check for Step Attribute
            if(v.step!="Null" && v.step!="undefined" && v.step!=undefined)
                field_attr+=' step="'+v.step+'"';
            // Check for Max-Len Attribute
            if(v.max_len!="Null" && v.max_len!="undefined" && v.max_len!=undefined)
                field_attr+=' max-len="'+v.max_len+'"';
            // Check for Required Attribute
            if(v.required!="Null" && v.required!=undefined && v.required!="undefined" && v.required=="True") 
                field_attr+=' required';
            return false;   // End the $.each Loop
        }
    });
    return field_attr;  //Return the Final String
}

function validateField(field, showErrors=true){
    if(field.attr("type") == "checkbox")
        return true;
    console.log(field.attr("type"));
    var val = field.val();
    var len = val.length;
    /** Check Required Attribute */
    if(field.attr("required")!="undefined" && field.attr("required")!=undefined){
        if(len==0){
            if(showErrors){
                field.tooltip({title:"This Field is required!", trigger:"manual", placement:"auto bottom"});
                field.tooltip('show');
                field.parent("div.form-group").removeClass("has-success").addClass("has-error");
            }
            return false;
        }
    }
    /** Check Min Attribute **/
    if(field.attr("min")!="undefined"){
        /** Check if it is a textfield **/
        if(field.attr("type")=="text"){
            if(len<parseInt(field.attr("min"))){
                if(showErrors){
                    field.tooltip({title:"Enter Atleast "+field.attr("min")+" characters", trigger:"manual", placement:"auto bottom"});
                    field.tooltip("show");
                    field.parent("div.form-group").removeClass("has-success").addClass("has-error");
                }
                return false
            }
        }else{
            /** If not a textfield **/
            val = field.val();
            min = field.attr("min");
            if(field.attr("type")=="number"){
                val = parseFloat(field.val());
                min = parseFloat(field.attr("min"));
            }
            if(val<min){
                if(showErrors){
                    field.tooltip({title:"Min allowed value is "+field.attr("min"), trigger: "manual", placement:"auto bottom"});   
                    field.tooltip("show");
                    field.parent("div.form-group").removeClass("has-success").addClass("has-error");
                }
                return false;
            }
        }
    }
    /** End Min Attribute **/
    /** Check Max Attribute **/
    if(field.attr("max")!="undefined"){
        /** Check if it is a textfield **/
        if(field.attr("type")=="text"){
            if(len>parseInt(field.attr("max"))){
                field.tooltip({title:"Max "+field.attr("max")+" characters allowed!", trigger: "manual", placement:"auto bottom"});
                field.tooltip("show");
                field.parent("div.form-group").removeClass("has-success").addClass("has-error");
                toReturn = false;
                return false;
            }
        }else{
            /** if not a textfield **/
            val = field.val();
            max = field.attr("max");
            if(field.attr("type")=="number"){
                val = parseFloat(field.val());
                max = parseFloat(field.attr("max"));
            }
            if(val>max){
                if(showErrors){
                    field.tooltip({title:"Max allowed value is "+field.attr("max"), trigger: "manual", placement:"auto bottom"});
                    field.tooltip("show");
                    field.parent("div.form-group").removeClass("has-success").addClass("has-error");
                }
                return false;
            }
        }
    }
    /** End Max Attribute **/
    /** Check Max-Len Attribute **/
    if(field.attr("max-len")!="undefined"){
        val = field.val();
        max_len = parseInt(field.attr("max-len"));
        if(val.length>max_len){
            if(showErrors){
                field.tooltip({title:"Max "+field.attr("max-len")+' characters allowed', trigger: "manual", placement:"auto bottom"});
                field.tooltip("show");
                field.parent("div.form-group").removeClass("has-success").addClass("has-error");
            }
            return false;
        }
    }
    /** End Max Len Attribute **/
    field.tooltip("hide");    //Hide tooltip if no errors were found
    field.parent("div.form-group").removeClass("has-error").addClass("has-success"); //Add Bootstrap has-success clas to the field
    return true;    //Return true
}

function filterGisDataByGroup(group_id, data){
    if(data==undefined)
        data = gisData;
    var filteredArray = [];
    if(group_id == "*")
        return data;
    $.each(data, function(index, value){
        if(value.data_group == group_id){
            filteredArray.push(value);
        }
    });
    return filteredArray;
}

function filterGisData(key, val, condition, group_id){
    /** Filter GisData and Return Array containing filtered data
     * 
     *  Data type and format remains same
     *  checks for key_type attribute for key
     */
    var filteredGisData = [];
    $.each(gisData, function(i,v){
        /** Iterate through gisData array 
         *  i: Contains Array Index
         *  v: Contains gisData Object
        **/
        if(v.data_group == group_id){
            $.each(v, function(index, value){
                /** Match keys to find Filter Key 
                 *  index: Contains Key Name from gisDataArray Object
                 *  value: Contains Value of the key 
                **/
                if(index == key){
                    var key_type = getKeyType(key);     //Get Key Type
                    if(key_type == "number"){
                        val = parseFloat(val);  //Parse as float if key_type is number
                        value = parseFloat(value);  //Parse as float if key_type is number
                    }
                    /** If Filter Key and gisData Key is natched **/
                    if(condition == "<"){
                        /** if Filter condition is 'Less Than' **/
                        if(value < val){
                            filteredGisData.push(v);
                        }
                    }
                    if(condition == ">"){
                        /** if Filter condition is 'Greater Than' **/
                        if(value > val){
                            filteredGisData.push(v);
                        }
                    }
                    if(condition == "="){
                        /** if Filter Condition is 'Equal to' **/
                        if(value == val){
                            filteredGisData.push(v);
                        }
                    }
                    if(condition == ">="){
                        /** if Filter Condition is 'Greater than or Equal to' **/
                        if(value >= val){
                            filteredGisData.push(v);
                        }
                    }
                    if(condition == "<="){
                        /** if Filter Condition is 'Less than or equal to' **/
                        if(value <= val){
                            filteredGisData.push(v);
                        }
                    }
                    return false;   //End $.each loop inner
                }
            }); 
        };
    });
    return filteredGisData;
}

function filterGisParametersByGroup(group_id, data){
    if(data==undefined)
        data = gisMetaFields;
    var filteredArray = [];
    if(group_id == "*")
        return data;
    $.each(data, function(index, value){
        if(value.data_group == group_id){
            filteredArray.push(value);
        }
    });
    return filteredArray;   
}

function getParameterGroupId(parameter_id){
    var toReturn = null;
    $.each(gisMetaFields, function(i,v){
        if(v.id == parameter_id){
            toReturn =  v.data_group;
            return false;
        }
    });
    return toReturn;
}

function getKeyType(key_name){
    /** Iterate through Meta Fields Array and return key_type on matching passed key */
    var key_type;
    $.each(gisMetaFields, function(i,v){
        if(v.key_name == key_name){
            key_type = v.key_type;
            return false;   //Break $.each loop
        }
    });
    return key_type;
}

function showNotification(msg, type){
    /** Shows Global Notification using notify.js */
    $.notify(msg, {position:"bottom left", className:type});
}