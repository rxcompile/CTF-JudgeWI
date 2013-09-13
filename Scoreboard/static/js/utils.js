function updatescores()
{
    $.ajax({
        url: '/scores'
        })
    .done(function(data) {
        $("#hor-zebra > tbody").empty();
        $("#hor-zebra > tbody:last").append(generatescores(data));
    })
    .fail(function() {
        //alert("error");
    });
}

function generatescores(data) {
    var ret = "";
    for( var i in data) {
        var t = data[i];
        if(i == 0){
            ret += "<tr class=\"first\">";
        } else if(i == 1) {
            ret += "<tr class=\"second\">";
        } else if(i == 2) {
            ret += "<tr class=\"third\">";
        } else {
            ret += "<tr class=\"other\">";
        }
        ret += "<td>" + t.place + "</td>";
        ret += "<td><a href='/team/" + t.team_id + "'>" + t.team + "</a></td>";
        ret += "<td class =\"logo\"><img src='" + t.team_image +"' class=\"images\"/></td>";
        for(var itdict in t.category) {
            var value = t.category[itdict];
            ret += "<td>" + value + "</td>";
        }
        ret +="<td>" + t.total_score + "</td>";
        ret +="</tr>";
    }
    return ret;
}

function updategrid(team_id, access) {
    $.ajax({
        url: '/tasks',
        data: {'team_id' : team_id}
    })
    .done(function(data) {
        $("#hor-zebra").empty();
        $("#hor-zebra").html(generategrid(data, access));
    })
    .fail(function() {
        //alert("error");
    });
}

function generategrid(data, access) {
    var ret = "";
    //alert("generategrid");
    for( var i in data) {
        var t = data[i];
        ret += "<tr><td class=\"name\">";
        ret += t.cat;
        ret += "</td>";
        for(var itdict in t.tasks) {
            var tdict = t.tasks[itdict];
            if(tdict.issolved) {
                ret += "<td class=\"solved\">";
            }
            else {
                ret += "<td class=\"tasks\">";
            }
            if(access) {
                ret += "<a href='#' onclick='checktask(" + tdict.task_id + ")'>" + tdict.task + "</a>";
            } else {
                ret += tdict.task;
            }
            ret += "</td>";
        }
        ret +="</tr>";
    }
    return ret;
}

function checktask(task_id) {
    $.ajax({
        url: '/tsk',
        data: {'task_id' : task_id }
    })
    .done(function(data) { 
        $('#overlay #content').empty();
        $('#overlay #content').append(data.task);
        $('#overlay #task_id').val(task_id);
        $('#overlay #flag').val("");
        if(!data.status)
            $('#sendform').removeClass('hidden');
        else
            $('#sendform').addClass('hidden');
        if(data.isFile != true) {
            $('#sendform #fileupload').addClass('hidden');
            $('#sendform #flag').removeClass('hidden');
        } else {
            $('#sendform #fileupload').removeClass('hidden');
            $('#sendform #flag').addClass('hidden');
        }
        $('#overlay').addClass('visible');
    })
    .fail(function() { 
        $('#overlay').removeClass('visible');
        alert("error");
    });
}

function send_flag() {
    var formData = new FormData($('#sendform')[0]);
    $.ajax({
        url: '/chk',  //server script to process data
        type: 'POST',
        xhr: function() {  // custom xhr
            myXhr = $.ajaxSettings.xhr();
            if(myXhr.upload){ // check if upload property exists
                //myXhr.upload.addEventListener('progress',progressHandlingFunction, false); // for handling the progress of the upload
            }
            return myXhr;
        },
        //Ajax events
        //beforeSend: beforeSendHandler,
        success: completeHandler,
        //error: errorHandler,
        // Form data
        data: formData,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

function completeHandler(data)
{ 
    if(data.status == 1) {
        $('#flag_accept').removeClass('hidden').fadeIn(200).delay(1500).fadeOut(200).queue(function(nxt){$('#overlay').removeClass('visible'); nxt();});
    } else if(data.status == 0) {
        $('#flag_reject').removeClass('hidden').fadeIn(200).delay(1500).fadeOut(200);
    } else {
        $('#flag_timeout #time').empty();
        $('#flag_timeout #time').append(30 - data.time);
        $('#flag_timeout').removeClass('hidden').fadeIn(200).delay(1500).fadeOut(200);
    }
}

function closeOverlay() {
    $('#overlay').removeClass('visible');
    $('#overlay #flag').val("");
}
