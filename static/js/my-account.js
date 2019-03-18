//codes below are used for safety check of the csrf token
var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// enable inputs and save button
function edit() {
    var inputs = document.getElementsByTagName("input");
    for (let i of inputs) {
        if (i.id !== "username")
            i.disabled = false;
    }
    $("#edit-btn").attr('disabled', 'disabled');
    $("#save-btn").removeAttr('disabled');
}

//submit the data in the inputs to the backend
function save() {
    var obj = {};
    obj.username = $("#username").val();
    obj.pref_name = $("#prefname").val();
    obj.email = $("#email").val();
    obj.phone = $("#phone").val();
    obj.address = $("#address").val();
    var is_valid = true;
    var inputs = document.getElementsByTagName("input");
    for (let i of inputs) {
        if (i.value === "") {
            is_valid = false;
            break;
        }
    }
    var jsonStr = JSON.stringify(obj);
    if (is_valid) {
        $.ajax({
            type: "post",
            url: '../edit-profile/',
            data: jsonStr,
            dataType: 'json',
            //if ajax succeed, show success info
            success: function () {
                M.toast({html: 'User details saved!'});
                for (i of inputs)
                    i.disabled = true;
                $("#save-btn").attr('disabled', 'disabled');
                $("#edit-btn").removeAttr('disabled');

            }
        });
    } else {
        //check the data integrity
        M.toast({html: 'Please finish all fields!'});
    }
}