M.AutoInit();
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
var idArr;
var qttArr;
var isDelivery;
var total = 0;
function update() {
    total = 0;
    var quantity_inputs = document.getElementsByName('quantity');
    $("#total_in_confirm_page").children().remove();
    idArr = [];
    qttArr = [];
    for (var i = 0; i < quantity_inputs.length; i++) {
        var curr = quantity_inputs[i];
        if (curr.value !== '0') {
            var custa_index = curr.id.substring(9,(curr.id.length-9));
            var quantity = curr.value;
            idArr.push(custa_index);
            qttArr.push(quantity);
        }
    }
    isDelivery = document.getElementById("id_is_delivery").checked;
    $("#cart").children().remove();     //remove all chidren first
    $("#order_details").children().remove();

    $("#total_price").text("");
    for (var i = 0; i < idArr.length; i++) {
        var custaname = document.createElement("td");
        custaname.innerText = $("#custa_" + idArr[i] + "_name").text();
        var custaprice = document.createElement("td");
        var custaqtt = document.createElement("td");
        custaqtt.innerText = $("#id_custa_" + idArr[i] + "_quantity").val();
        custaprice.innerText = "£"+(parseFloat($("#id_custa_" + idArr[i] + "_price").text().substring(1)) * parseInt(custaqtt.innerText)).toFixed(2);
        total += parseFloat($("#id_custa_" + idArr[i] + "_price").text().substring(1)) * parseInt(custaqtt.innerText);
        var trEle = document.createElement("tr");
        trEle.append(custaname);
        trEle.append(custaprice);
        trEle.append(custaqtt);
        $("#cart").append(trEle);
        var trEle_cloned = trEle.cloneNode(true);
        $("#order_details").append(trEle_cloned);
    }
    if(isDelivery && total!==0)
        total+=2;
    var totalStr = "Total: £" + total.toFixed(2);
    $("#total_price").text(totalStr);
    var text_deliveryfee = document.createElement("p");
    text_deliveryfee.innerText="Delivery Fee: £2.00";
    var text_total =  document.createElement("p");
    text_total.className = "big-font";
    text_total.innerText = totalStr;
    if(isDelivery){
        $("#total_in_confirm_page").append(text_deliveryfee);
    }
    $("#total_in_confirm_page").append(text_total);
    if(total===0)
        $("#goto_checkout").attr('disabled', 'disabled');
    else{
        $("#goto_checkout").removeAttr('disabled');
    }
}

function checkout() {
    update();
    var obj = {};
    obj.idArray = idArr;
    obj.quantityArray = qttArr;
    obj.isDelivery = isDelivery;
    obj.total = total;
    var jsonStr = JSON.stringify(obj);
    console.log(jsonStr);
    if (total!==0) {
        $.ajax({
            type: "post",
            url: '../checkout/',
            data: jsonStr,
            dataType: 'json',
            success: function () {
                $("#modal1_content").children().remove();
                var success_container = document.createElement("div");
                success_container.className = "card-panel";
                var success_info = document.createElement("h3");
                success_info.innerText = "Your order has been placed.";
                var success_icon = document.createElement("i");
                success_icon.className = "material-icons";
                success_icon.style = "font-size: 10rem; color: green;";
                success_icon.innerText = "check";
                success_container.appendChild(success_icon);
                success_container.appendChild(success_info);
                $("#modal1_content").append(success_container);
                var back_button = document.createElement("a");
                back_button.className = "btn-large waves-effect";
                back_button.innerText = "OK";
                back_button.href = "../order/";
                $("#modal_footer").children().remove();
                $("#modal_footer").append(back_button);
            }
        });
    }
}

function increase(textID) {
    var ele = $("#" + textID);
    var ele_num = ele.val();
    ele.val(ele_num * 1 + 1);
    update();
}

function decrease(textID) {
    var ele = $("#" + textID);
    var ele_num = ele.val();
    if (ele_num > 0) {
        ele.val(ele_num * 1 - 1);
    }
    update();
}
