showPrice();
showType();

//calculate and show the real price in pounds
function showPrice() {
    var price_components = document.getElementsByClassName('price');
    for(let c of price_components){
        var price = c.innerText;
        var realPrice = "£" + (parseFloat(price) / 100);
        c.innerText = realPrice;
    }
}

//show the type of order - delivery/pick-up
function showType() {
    var type_components = document.getElementsByClassName('ordertype');
    for (let t of type_components){
        var text = t.innerText;
        if(text==="False"){
            t.innerText = "Pickup";
        }else {
            t.innerText = "Delivery";
        }
    }
}
