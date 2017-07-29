var apiURI = '/portal/ajax/';

function getmetafields(callbackFunc){
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