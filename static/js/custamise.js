M.AutoInit();
function calcTotal() {
    var selected_base_id = $("input[name='base']:checked").val();
    var basePrice;
    $("#id_tags").html("");
    if (selected_base_id !== undefined) {
        basePrice = (baseList[selected_base_id - 1].price) / 100;
        var basetag = "<div class='chip'>"+ baseList[selected_base_id-1].name +"</div>";
        $("#id_tags").append(basetag);
    } else {
        basePrice = 0;
    }
    var selected_sauce_id = $("input[name='sauce']:checked").val();
    var saucePrice;
    if (selected_sauce_id !== undefined) {
        saucePrice = (sauceList[selected_sauce_id - 1].price) / 100;
        var saucetag = "<div class='chip'>"+ sauceList[selected_sauce_id-1].name +"</div>";
        $("#id_tags").append(saucetag);
    }
    else
        saucePrice = 0;
    var selected_top_id = $("input[name='top']:checked").val();
    var topPrice;
    if (selected_top_id !== undefined) {
        topPrice = (topList[selected_top_id - 1].price) / 100;
        var toptag = "<div class='chip'>"+ topList[selected_top_id-1].name +"</div>";
        $("#id_tags").append(toptag);
    }
    else
        topPrice = 0;
    var total = basePrice + saucePrice + topPrice;
    $("#id_price").val(total*100);
    $("#price_label").html("Price: £ " + total.toFixed(2));
}

function openSection(index) {
    $('.collapsible').collapsible('open', index);
}

function nextSection(index) {
    var checked = false;
    var type;
    if(index===0){
        type = "base";
    }else if(index===1){
        type = "sauce";
    }else{
        type = "top";
    }
    var radios = document.getElementsByName(type);
    for(var i=0; i<radios.length; i++){
        checked = checked || radios[i].checked;
    }
    if(!checked){
        M.toast({html: 'please select a ' + type});
    }else{
        if(index===2){
            document.getElementById('id_name').focus();
        }else{
            openSection(index+1);
        }
    }
}
