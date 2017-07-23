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