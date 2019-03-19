M.AutoInit();
//used for the safety check of csrf token
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

//global variables...
var idArr;
var qttArr;
var isDelivery;
var total = 0;

// helper function to update all information including total price, list showing in the cart panel.
// should be called whenever user make changes to the order details.
function update() {
    total = 0;
    var quantity_inputs = document.getElementsByClassName('medium-font');
    //remove all children first
    $("#total_in_confirm_page").children().remove();
    idArr = [];
    qttArr = [];
    //for each input of quantity
    for (var i = 0; i < quantity_inputs.length; i++) {
        var curr = quantity_inputs[i];
        // if current input's quantity is not 0, add it to cart
        if (curr.textContent !== '0') {
            var custa_index = curr.id.substring(9, (curr.id.length - 9));
            var quantity = curr.textContent;
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
        custaname.style = "max-width: 165px";
        custaname.innerText = $("#custa_" + idArr[i] + "_name").text();
        var custaprice = document.createElement("td");
        var custaqtt = document.createElement("td");
        custaqtt.innerText = $("#id_custa_" + idArr[i] + "_quantity").text();
        custaprice.innerText = "£" + (parseFloat($("#id_custa_" + idArr[i] + "_price").text().substring(1)) * parseInt(custaqtt.innerText)).toFixed(2);
        total += parseFloat($("#id_custa_" + idArr[i] + "_price").text().substring(1)) * parseInt(custaqtt.innerText);
        var trEle = document.createElement("tr");
        trEle.append(custaname);
        trEle.append(custaprice);
        trEle.append(custaqtt);
        $("#cart").append(trEle);
        var trEle_cloned = trEle.cloneNode(true);
        $("#order_details").append(trEle_cloned);
    }
    // if it's delivery order, add 2 pounds for delivery fee
    if (isDelivery && total !== 0)
        total += 2;
    var totalStr = "Total: £" + total.toFixed(2);
    $("#total_price").text(totalStr);
    var text_deliveryfee = document.createElement("p");
    text_deliveryfee.innerText = "Delivery Fee: £2.00";
    var text_total = document.createElement("p");
    text_total.className = "big-font";
    text_total.innerText = totalStr;
    // add everything to the html DOM
    if (isDelivery) {
        $("#total_in_confirm_page").append(text_deliveryfee);
    }
    $("#total_in_confirm_page").append(text_total);
    if (total === 0) {
        $("#goto_checkout").attr('disabled', 'disabled');
        $("#goto_checkout_mobile").attr('disabled', 'disabled');
    } else {
        $("#goto_checkout").removeAttr('disabled');
        $("#goto_checkout_mobile").removeAttr('disabled');
    }
}
var panelVisible = true;
function hideOrShow(){
	if(panelVisible){
		$("#cart_panel").hide();
		panelVisible = false;
	}else {
		$("#cart_panel").show();
		panelVisible = true;
	}
}

// function used to handle checkout, using ajax to pass data to the back-end
function checkout() {
    update();       //call update() first to make sure everything is up-to-date
    var obj = {};   //create object for transmitting
    obj.idArray = idArr;
    obj.quantityArray = qttArr;
    obj.isDelivery = isDelivery;
    obj.total = total;
    var jsonStr = JSON.stringify(obj);
    //checkout action is only approved when there's item in the cart
    if (total !== 0) {
        $.ajax({
            type: "post",
            url: '../checkout/',
            data: jsonStr,
            dataType: 'json',
            //if success
            success: function () {
                // remove everything in the modal first
                $("#modal1_content").children().remove();
                //codes below shows actions of adding DOMs to modal which show success information
                var success_container = document.createElement("div");
                success_container.className = "card-panel";
                var success_info = document.createElement("div");
                success_info.innerText = "Your order has been placed.";
                success_info.className = "big-font";
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
                //redirect back to index
                back_button.href = "../";
                $("#modal_footer").children().remove();
                $("#modal_footer").append(back_button);
            }
        });
    }
}

//method bonded to switch click event
function syncSwitch(switchIndex) {
    if (switchIndex === 1) {  //if it's the switch in the cart
        update();         //update first
        document.getElementById("id_is_delivery_mobile").checked = document.getElementById("id_is_delivery").checked;
    } else {          //if it's the mobile one
        document.getElementById("id_is_delivery").checked = document.getElementById("id_is_delivery_mobile").checked;
        update();   //update after the cart one is synchronized
    }
}

//method to add a corresponding custa
function increase(textID) {
    var ele = $("#" + textID);
    var ele_num = ele.text();
    ele.text(ele_num * 1 + 1);
    update();
}

//method to delete a corresponding custa
function decrease(textID) {
    var ele = $("#" + textID);
    var ele_num = ele.text();
    // custa number cannot be negative
    if (ele_num > 0) {
        ele.text(ele_num * 1 - 1);
    }
    update();
}

