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
            $('#sendform').addClass('visible');
        else
            $('#sendform').removeClass('visible');
        if(data.isFile)
            $('#sendform #file').addClass('visible');
        else
            $('#sendform #file').removeClass('visible');
        $('#overlay').addClass('visible');
    })
    .fail(function() { 
        $('#overlay').removeClass('visible');
        alert("error");
    });
}

function sendflag(task_id, flag) {
    $.ajax({
        url: '/chk',
        data: {'task_id' : task_id, 'flag' : flag }
    })
    .done(function(data) {
        if(data.status)
            $('#overlay #flag').val('Флаг принят');
        else
            $('#overlay #flag').val('Флаг не принят');
        //$('#overlay #farm').removeClass('visible');
    })
    .fail(function() {
        alert("error");
    });
}

function closeOverlay() {
    $('#overlay').removeClass('visible');
    $('#overlay #flag').val("");
}
