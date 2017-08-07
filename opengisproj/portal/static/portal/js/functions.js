var apiURI = '/portal/ajax/';

function getMetaFields(callbackFunc){
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

}

function storeGisGroups(data){
    gisGroups = data;
    gis_groups_stored = true;
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
    var val = field.val();
    var len = val.length;
    /** Check Required Attribute */
    if(field.attr("required")!="undefined"){
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

function showNotification(msg, type){
    $.notify(msg, {position:"bottom left", className:type});
}